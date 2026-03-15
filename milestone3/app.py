import base64
import streamlit as st
import re
from pathlib import Path
from dotenv import load_dotenv

from prompt_builder import build_prompt
from model_api import query_model
from diet_builder import build_diet_prompt
from auth import generate_otp, create_jwt, verify_jwt
from email_utils import send_otp_email


load_dotenv()

st.set_page_config(page_title="FitPlan AI", layout="wide")


# --- GLOBAL STYLES ---
st.markdown(
    """
    <style>
    header {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at top left, #ffecd2 0%, #fcb69f 25%, #f6d365 60%, #fda085 100%);
        background-attachment: fixed;
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020024 0%, #090979 40%, #00d4ff 100%) !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    .login-card {
        background: rgba(255,255,255,0.96);
        padding: 40px 35px;
        border-radius: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
    }

    .login-title {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(90deg, #004d57, #ff7e5f);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 10px;
    }

    .login-subtitle {
        font-size: 15px;
        color: #636e72;
        margin-bottom: 25px;
    }

    .proverb {
        font-size: 20px;
        font-style: italic;
        font-weight: 600;
        color: #ffffff;
        text-shadow: 0 4px 16px rgba(0,0,0,0.35);
        margin-top: 20px;
    }

    .assessment-card {
        background-color: white !important;
        padding: 25px;
        border-radius: 18px;
        border-left: 10px solid #004d57;
        color: #000000 !important;
        margin-bottom: 30px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    }

    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        border-top: 5px solid #004d57;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    }

    .stat-card h3 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
    }

    .stat-card p {
        margin-top: 6px;
        font-size: 13px;
        letter-spacing: 2px;
        color: #7f8c8d;
    }

    /* --- CARD MODULE STYLES --- */
    .day-container {
        background-color: white !important;
        padding: 30px;
        border-radius: 25px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: #2d3436;
    }

    .day-header {
        color: #004d57;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .item-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 0;
        border-bottom: 1px solid #f1f1f1;
    }

    .item-row:last-child {
        border-bottom: none;
    }

    .ex-name {
        flex: 2;
        font-weight: 600;
        color: #2d3436;
        font-size: 18px;
    }

    .stat-group {
        display: flex;
        gap: 15px;
        flex: 1.5;
        justify-content: flex-end;
    }

    .stat-pill {
        text-align: center;
        min-width: 75px;
        background: #f8f9fa;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #eee;
    }

    .stat-val {
        color: #004d57;
        font-weight: bold;
        font-size: 15px;
        display: block;
    }

    .stat-label {
        font-size: 10px;
        color: #636e72;
        text-transform: uppercase;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


BASE_DIR = Path(__file__).parent
LOGIN_BG_PATH = BASE_DIR / "assets" / "login_bg.png"


def _load_login_background() -> str:
    try:
        with open(LOGIN_BG_PATH, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""


_login_bg_base64 = _load_login_background()

if _login_bg_base64:
    st.markdown(
        f"""
        <style>
        .login-hero {{
            background-image: linear-gradient(
                    to bottom right,
                    rgba(0, 0, 0, 0.35),
                    rgba(0, 0, 0, 0.8)
                ),
                url("data:image/png;base64,{_login_bg_base64}");
            background-size: cover;
            background-position: center;
            border-radius: 28px;
            min-height: 420px;
            height: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- UTILITY FUNCTIONS ---
def parse_plan_to_json(text: str, is_diet: bool = False):
    """Parses raw text into structured JSON for Workout or Diet cards."""
    sections = []
    pattern = r"(Day \d+:.*)" if not is_diet else r"(Meal \d+:.*|Breakfast:|Lunch:|Dinner:|Snack:)"
    parts = re.split(pattern, text)

    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            header = parts[i].strip()
            if i + 1 >= len(parts):
                continue
            content = parts[i + 1].strip()
            items = []
            lines = content.split("\n")
            for line in lines:
                if line.strip().startswith(("-", "*")):
                    main_part = line.strip("- *").split("|")[0].split(":")[0].strip()
                    items.append(
                        {
                            "name": main_part,
                            "val1": "3 sets" if not is_diet else "1 bowl",
                            "val2": "10 reps" if not is_diet else "300 kcal",
                            "val3": "60s" if not is_diet else "High Protein",
                        }
                    )
            sections.append({"header": header, "items": items})
    return sections


def render_cards(data, label1: str, label2: str, label3: str):
    """Renders data into the card UI with custom labels for Workout or Diet."""
    for section in data:
        st.markdown(
            f"""
            <div class="day-container">
                <div class="day-header">🗓️ {section['header']}</div>
            """,
            unsafe_allow_html=True,
        )

        for item in section["items"]:
            st.markdown(
                f"""
                <div class="item-row">
                    <div class="ex-name">🔘 {item['name']}</div>
                    <div class="stat-group">
                        <div class="stat-pill"><span class="stat-val">{item['val1']}</span><span class="stat-label">{label1}</span></div>
                        <div class="stat-pill"><span class="stat-val">{item['val2']}</span><span class="stat-label">{label2}</span></div>
                        <div class="stat-pill"><span class="stat-val">{item['val3']}</span><span class="stat-label">{label3}</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


# --- SESSION STATE INITIALIZATION ---
if "otp" not in st.session_state:
    st.session_state.otp = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None
if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None


# --- LOGIN PAGE (PHASE 1) ---
if not st.session_state.authenticated:
    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            """
            <div class="login-hero">
                <div style="padding: 40px 35px;">
                    <div class="login-title">FitPlan AI</div>
                    <div class="login-subtitle">
                        An AI-powered fitness and diet planner tailored to your goals.<br/>
                        Track your journey, stay consistent, and watch yourself transform.
                    </div>
                    <div class="proverb">
                        "The body achieves what the mind believes."
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Login to your AI Fitness Hub")
        email = st.text_input("Email address", placeholder="you@example.com")

        if st.button("Send OTP", use_container_width=True):
            if email:
                otp = generate_otp()
                st.session_state.otp = otp
                st.session_state.email = email
                try:
                    send_otp_email(email, otp)
                    st.success("OTP sent to your email.")
                except Exception:
                    st.error("Failed to send email. Check your SendGrid settings.")
            else:
                st.error("Please enter your email.")

        if st.session_state.otp:
            entered_otp = st.text_input("Enter OTP", type="password")
            if st.button("Verify OTP", use_container_width=True):
                if entered_otp == st.session_state.otp:
                    st.session_state.token = create_jwt(st.session_state.email)
                    st.session_state.authenticated = True
                    st.success("Login successful! Redirecting to your dashboard...")
                    st.rerun()
                else:
                    st.error("Invalid OTP.")

        st.markdown("</div>", unsafe_allow_html=True)


# --- MAIN APP (PHASE 2) ---
else:
    decoded = verify_jwt(st.session_state.token)
    if not decoded:
        st.session_state.authenticated = False
        st.error("Session expired. Please login again.")
        st.rerun()

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("## 👟 FitPlan AI")
        st.write(f"**Logged in as:** {decoded['email']}")
        st.write("---")

        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()
        if st.button("🏋️ Workout Plan", use_container_width=True):
            st.session_state.page = "result" if st.session_state.workout_plan else "input"
            st.rerun()
        if st.button("🥗 Dietary Plan", use_container_width=True):
            st.session_state.page = "diet"
            st.rerun()

        st.write("---")
        if st.button("🔄 New Fitness Journey", use_container_width=True):
            st.session_state.workout_plan = None
            st.session_state.diet_plan = None
            st.session_state.user_data = None
            st.session_state.page = "profile"
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.otp = None
            st.rerun()

    # --- DASHBOARD PAGE ---
    if st.session_state.page == "dashboard":
        st.markdown("### 📊 Your Fitness Dashboard")
        if st.session_state.user_data:
            d = st.session_state.user_data
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f'<div class="stat-card"><h3>{d["name"]}</h3><p>USER</p></div>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f'<div class="stat-card"><h3>{d["bmi"]:.1f}</h3><p>BMI</p></div>',
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f'<div class="stat-card"><h3 style="color:{d["color"]}">{d["status"]}</h3><p>HEALTH</p></div>',
                    unsafe_allow_html=True,
                )

            st.write("")
            st.markdown(
                """
                <div class="assessment-card">
                    <h3 style="margin-bottom:6px;">Progress Snapshot</h3>
                    <p style="margin:0;color:#636e72;">
                        Stay consistent, hydrate well, and fuel your body correctly.
                        Your personalized workout and dietary plans are just a click away.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No profile data yet. Go to the Profile tab to create your fitness profile.")

    # --- PROFILE PAGE ---
    elif st.session_state.page == "profile":
        st.markdown("### 👤 Your Fitness Profile")
        st.caption("Tell FitPlan AI about you so it can generate the most accurate workout and diet plans.")

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            name = st.text_input("Name", value=(st.session_state.user_data or {}).get("name", ""))
        with c2:
            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=0,
            )
        with c3:
            age = st.number_input("Age", min_value=1, value=19)

        h, w = st.columns(2)
        with h:
            height = st.number_input("Height (cm)", value=170.0)
        with w:
            weight = st.number_input("Weight (kg)", value=70.0)

        goal = st.selectbox(
            "Primary Goal",
            ["Build Muscle", "Weight Loss", "Strength", "Flexibility"],
        )
        level = st.selectbox(
            "Fitness Level",
            ["Beginner", "Intermediate", "Advanced"],
        )
        equip = st.multiselect(
            "Available Equipment",
            ["Dumbbells", "Kettlebells", "Pull-up Bar", "Resistance Bands", "Yoga Mat", "No Equipment"],
        )

        st.write("")
        col_a, col_b = st.columns([1, 1])

        if col_a.button("💾 Save Profile", use_container_width=True):
            prompt, bmi, status, color = build_prompt(
                name, gender, age, height, weight, goal, level, equip
            )
            st.session_state.user_data = {
                "name": name,
                "bmi": bmi,
                "status": status,
                "color": color,
                "goal": goal,
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "level": level,
                "equip": equip,
            }
            st.success("Profile saved. You can now generate your workout and diet plans.")

        if col_b.button("🚀 Generate Complete Plan", use_container_width=True):
            if name.strip() == "":
                st.error("Please enter your name before generating a plan.")
            else:
                prompt, bmi, status, color = build_prompt(
                    name, gender, age, height, weight, goal, level, equip
                )
                prompt += "\nFormat: Day X: [Name]\n- [Exercise]: [Sets], [Reps], [Rest]"
                with st.spinner("AI is crafting your personalised routine..."):
                    st.session_state.workout_plan = query_model(prompt)
                    st.session_state.user_data = {
                        "name": name,
                        "bmi": bmi,
                        "status": status,
                        "color": color,
                        "goal": goal,
                        "gender": gender,
                        "age": age,
                        "height": height,
                        "weight": weight,
                        "level": level,
                        "equip": equip,
                    }
                    st.session_state.page = "result"
                    st.rerun()

    # --- WORKOUT RESULT PAGE ---
    elif st.session_state.page == "result":
        if not st.session_state.user_data or not st.session_state.workout_plan:
            st.info("No workout plan yet. Go to the Profile tab and generate a plan first.")
        else:
            d = st.session_state.user_data
            st.markdown(
                f'<div class="assessment-card"><h2>Hello {d["name"]}</h2>'
                f'<p>BMI: {d["bmi"]:.2f} | {d["status"]}</p>'
                f'<p style="margin-top:6px;color:#636e72;">Goal: {d["goal"]}</p></div>',
                unsafe_allow_html=True,
            )

            st.download_button(
                "📥 Download Workout Plan",
                st.session_state.workout_plan,
                file_name="workout_plan.txt",
            )

            plan_json = parse_plan_to_json(st.session_state.workout_plan)
            if plan_json:
                render_cards(plan_json, "SETS", "REPS", "REST")
            else:
                st.write(st.session_state.workout_plan)

    # --- DIET PAGE ---
    elif st.session_state.page == "diet":
        st.markdown("### 🥗 Dietary Plan")
        if st.session_state.user_data:
            if not st.session_state.diet_plan:
                d = st.session_state.user_data
                d_prompt = build_diet_prompt(
                    d["name"], d.get("gender", "User"), d.get("age", 20), d.get("height", 170), d.get("weight", 70), d["goal"]
                )
                with st.spinner("AI is generating your diet plan..."):
                    st.session_state.diet_plan = query_model(d_prompt)

            st.download_button(
                "📥 Download Diet Plan",
                st.session_state.diet_plan,
                file_name="diet_plan.txt",
            )

            diet_json = parse_plan_to_json(st.session_state.diet_plan, is_diet=True)
            if diet_json:
                render_cards(diet_json, "PORTION", "CALORIES", "TYPE")
            else:
                st.write(st.session_state.diet_plan)
        else:
            st.info("Create and save your profile first in the Profile tab to get a diet plan.")


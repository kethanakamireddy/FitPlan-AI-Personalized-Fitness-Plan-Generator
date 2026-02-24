import streamlit as st
from datetime import datetime
from prompt_builder import build_prompt, bmi_category  # Import from prompt_builder
from model_api import query_model  # Import the model API

st.set_page_config(
    page_title="FIT Plan AI - Milestone 1",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FIT Plan AI – Personalized Fitness Profile")
st.markdown("---")

# Initialize session state
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None

with st.form("fitness_profile_form"):
    st.header("📋 Your Fitness Profile")
    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name *")
        height = st.number_input("Height (cm) *", min_value=1.0, max_value=300.0, value=170.0)

    with col2:
        age = st.number_input("Age", min_value=10, max_value=120, value=25)
        weight = st.number_input("Weight (kg) *", min_value=1.0, max_value=500.0, value=70.0)

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    st.subheader("🎯 Fitness Details")

    goal = st.selectbox(
        "Fitness Goal *",
        ["Weight Loss", "Build Muscle", "Strength Gain", "Abs Building", "Flexibility"]
    )

    equipment = st.multiselect(
        "Available Equipment *",
        [
            "Dumbbells",
            "Resistance Bands",
            "Barbell",
            "Pull-up Bar",
            "Treadmill",
            "Kettlebells",
            "Jump Rope",
            "Yoga Mat",
            "No Equipment (Bodyweight only)"
        ],
        default=["No Equipment (Bodyweight only)"]
    )

    fitness_level = st.select_slider(
        "Fitness Level *",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )

    st.markdown("---")
    submit = st.form_submit_button("Submit Profile", use_container_width=True)

if submit:
    if not name:
        st.error("Please enter your name.")
        st.stop()

    if not equipment:
        st.error("Please select at least one equipment option.")
        st.stop()

    # Build prompt using the imported function
    prompt, bmi, bmi_status = build_prompt(
        name=name,
        gender=gender,
        height=height,
        weight=weight,
        goal=goal,
        fitness_level=fitness_level,
        equipment=equipment
    )

    st.success("✅ Profile Submitted Successfully!")

    st.session_state.update({
        "form_submitted": True,
        "name": name,
        "bmi": bmi,
        "bmi_status": bmi_status,
        "age": age,
        "goal": goal,
        "equipment": equipment,
        "fitness_level": fitness_level,
        "height": height,
        "weight": weight,
        "gender": gender,
        "prompt": prompt  # Store the generated prompt
    })

if st.session_state.form_submitted:
    st.markdown("---")
    st.success(f"Welcome, *{st.session_state.name}*!")

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 BMI", f"{st.session_state.bmi:.2f}")
    col2.metric("🏷 Category", st.session_state.bmi_status)
    col3.metric("🏋️ Level", st.session_state.fitness_level)

    # Generate Workout Plan Button
    st.markdown("---")
    st.subheader("🏋️ Generate Your Personalized Workout Plan")
    
    if st.button("Generate Workout Plan", type="primary", use_container_width=True):
        with st.spinner("Creating your personalized workout plan... This may take a moment."):
            # Call the model API
            workout_plan = query_model(st.session_state.prompt)
            st.session_state.workout_plan = workout_plan
        
    # Display workout plan if generated
    if st.session_state.workout_plan:
        st.markdown("---")
        st.subheader("📋 Your 5-Day Workout Plan")
        
        with st.container():
            st.markdown(st.session_state.workout_plan)
        
        # Download button for workout plan
        workout_text = f"""
FIT PLAN AI - PERSONALIZED WORKOUT PLAN
Generated for: {st.session_state.name}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Profile Summary:
- BMI: {st.session_state.bmi:.2f} ({st.session_state.bmi_status})
- Goal: {st.session_state.goal}
- Level: {st.session_state.fitness_level}
- Equipment: {', '.join(st.session_state.equipment)}
{st.session_state.workout_plan}
---
Stay consistent and trust the process!
"""
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Workout Plan",
                data=workout_text,
                file_name=f"FITPlanAI_{st.session_state.name}_Workout.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            if st.button("Generate New Plan", use_container_width=True):
                st.session_state.workout_plan = None
                st.rerun()

    # Profile Report Section
    st.markdown("---")
    with st.expander("📄 View Profile Report"):
        report_text = f"""
FIT PLAN AI - PROFILE REPORT
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Name: {st.session_state.name}
Age: {st.session_state.age}
Gender: {st.session_state.gender}
Height: {st.session_state.height} cm
Weight: {st.session_state.weight} kg
BMI: {st.session_state.bmi:.2f}
Category: {st.session_state.bmi_status}
Goal: {st.session_state.goal}
Level: {st.session_state.fitness_level}
Equipment: {', '.join(st.session_state.equipment)}
Stay consistent and trust the process!
"""

        st.download_button(
            "📥 Download Profile Report",
            data=report_text,
            file_name=f"FITPlanAI_{st.session_state.name}_Profile.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.caption("FIT Plan AI - Milestone 1 | Powered by Mistral-7B")

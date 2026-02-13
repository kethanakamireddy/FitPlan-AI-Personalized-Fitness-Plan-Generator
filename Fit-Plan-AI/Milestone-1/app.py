import streamlit as st

# ---------- Page Title ----------
st.set_page_config(page_title="FitPlan AI - Milestone 1")

st.title("🏋️ FitPlan AI - Personalized Fitness Profile")

st.write("Enter your details to calculate your BMI and health category.")

# ---------- Form ----------
with st.form("fitness_form"):

    st.subheader("Personal Information")

    name = st.text_input("Name *")
    height_cm = st.number_input("Height (in centimeters) *", min_value=0.0)
    weight_kg = st.number_input("Weight (in kilograms) *", min_value=0.0)

    st.subheader("Fitness Details")

    fitness_goal = st.selectbox(
        "Fitness Goal",
        ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"]
    )

    equipment = st.multiselect(
        "Available Equipment",
        ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment", "Kettlebell", "Barbell"]
    )

    fitness_level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    submit = st.form_submit_button("Submit")

# ---------- Validation & Logic ----------
if submit:

    if name.strip() == "":
        st.error("Name is required.")

    elif height_cm <= 0 or weight_kg <= 0:
        st.error("Height and Weight must be positive values.")

    else:
        # Convert height from cm to meters
        height_m = height_cm / 100

        # BMI calculation
        bmi = weight_kg / (height_m ** 2)

        # Round to 2 decimal places
        bmi = round(bmi, 2)

        # BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        # ---------- Output ----------
        st.success("Profile submitted successfully!")

        st.write(f"👤 Name: {name}")
        st.write(f"📏 Height: {height_cm} cm")
        st.write(f"⚖️ Weight: {weight_kg} kg")
        st.write(f"🎯 Goal: {fitness_goal}")
        st.write(f"🏋️ Fitness Level: {fitness_level}")
        st.write(f"🧰 Equipment: {', '.join(equipment) if equipment else 'None'}")

        st.markdown("---")

        st.subheader("📊 BMI Result")
        st.write(f"**{name}'s BMI:** {bmi}")
        st.write(f"**Category:** {category}")

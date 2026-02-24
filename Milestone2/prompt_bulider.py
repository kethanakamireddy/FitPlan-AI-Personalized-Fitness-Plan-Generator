def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def build_prompt(name, gender, height, weight, goal, fitness_level, equipment):

    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    prompt = f"""
You are a certified professional fitness trainer.
Create a structured 5-day personalized workout plan.
User Profile:
- Name: {name}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.2f} ({bmi_status})
- Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}
Instructions:
1. Divide clearly into Day 1 to Day 5.
2. Include exercise name.
3. Include sets and reps.
4. Include rest period.
5. Adjust intensity based on BMI category.
6. Avoid unsafe exercises for beginners.
7. Keep the plan professional and easy to follow.
"""

    return prompt, bmi, bmi_status


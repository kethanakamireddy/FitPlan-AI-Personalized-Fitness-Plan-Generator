def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db"
    elif bmi < 25:
        return "Normal Weight", "#2ecc71"
    elif bmi < 30:
        return "Overweight", "#f1c40f"
    else:
        return "Obese", "#e74c3c"

def build_prompt(name, gender, age, height, weight, goal, fitness_level, equipment):
    bmi = calculate_bmi(weight, height)
    bmi_status, status_color = bmi_category(bmi)
    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    prompt = f"""You are a professional trainer. Create a 5-day plan for {name}.
User Profile: Age {age}, Gender {gender}, BMI {bmi:.2f}, Goal {goal}, Level {fitness_level}, Equipment {equipment_list}.
STRICT FORMATTING RULES:
1. Label days as Day 1:, Day 2:, etc.
2. For EVERY exercise, use this EXACT format:
   - Exercise Name | Sets | Reps | Rest
3. Example: - Dumbbell Bench Press | 3 | 10-12 | 60s
4. Day 3 must be "Rest Day".
5. Do not include any intro or outro text. Output only the days and exercises."""

    return prompt, bmi, bmi_status, status_color

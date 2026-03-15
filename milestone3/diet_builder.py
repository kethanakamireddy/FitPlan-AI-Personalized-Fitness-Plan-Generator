def build_diet_prompt(name, gender, age, height, weight, goal):
    bmi = weight / ((height / 100) ** 2)
    
    if goal == "Weight Loss":
        diet_type = "Low carb, high protein, 500 calorie deficit"
    elif goal == "Build Muscle":
        diet_type = "High carb, high protein, 300 calorie surplus"
    else:
        diet_type = "Balanced macros, maintenance calories"

    prompt = f"""
    Act as a professional nutritionist for {name}.
    Stats: BMI {bmi:.1f}, Goal: {goal}, Strategy: {diet_type}.
    
    STRICT FORMAT:
    Day 1: Daily Nutrition Plan
    - Meal Name : Time, Calories, Notes
    
    Provide 4 unique meals. Use the ':' and ',' format exactly as shown above.
    Do not include any introductory or concluding text.
    """
    return prompt

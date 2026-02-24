def build_prompt(name, age, bmi, goal, level, equipment):
    
    prompt = f"""
    Create a personalized 7-day workout plan.

    User Details:
    Name: {name}
    Age: {age}
    BMI Category: {bmi}
    Fitness Goal: {goal}
    Fitness Level: {level}
    Available Equipment: {equipment}

    Instructions:
    - Provide daily workout plan (Day 1 to Day 7)
    - Include warm-up and cool-down
    - Mention sets and reps
    - Keep it safe and beginner friendly if needed
    - Give short diet suggestion
    """

    return prompt

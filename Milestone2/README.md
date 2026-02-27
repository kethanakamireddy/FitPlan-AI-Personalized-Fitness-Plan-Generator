# 🏋️ FitPlan AI – Milestone 2: Core AI Model Integration

## 📌 Objective of the Milestone

The objective of Milestone 2 is to integrate a pre-trained Large Language Model (LLM) from Hugging Face into the FitPlan AI application to dynamically generate personalized workout plans based on user fitness inputs collected in Milestone 1.

This milestone ensures:
- Successful integration of a Hugging Face LLM
- Structured dynamic prompt construction
- Personalized workout plan generation
- Deployment using Streamlit on Hugging Face Spaces

---

## 🤖 Model Used

- *Model Name:* google/flan-t5-base  
- *Library:* Hugging Face Transformers  
- *Pipeline:* text2text-generation  

### Reason for Selecting This Model:
- Lightweight and suitable for CPU environments
- Good instruction-following capability
- Compatible with Hugging Face Spaces (Free Tier)

---

## 🧠 Prompt Design Explanation

A structured dynamic prompt is created using the following user inputs:

- Name  
- Age  
- BMI Category  
- Fitness Goal  
- Fitness Level  
- Available Equipment  

### 🔹 Prompt Strategy

The model is instructed to:

- Generate a structured 7-day workout plan
- Include warm-up and cool-down routines
- Mention sets and repetitions
- Ensure safety based on fitness level
- Provide a short diet suggestion

This structured prompt ensures personalized and goal-oriented output.

---

## ⚙️ Steps Performed

### 1️⃣ Model Loading
- Installed required libraries (transformers, torch, streamlit)
- Loaded model using Hugging Face pipeline
- Cached model using @st.cache_resource for performance optimization

### 2️⃣ Prompt Creation
- Created a separate module prompt_builder.py
- Constructed dynamic prompt using user inputs
- Maintained clean and modular code structure

### 3️⃣ Inference Testing
- Generated workout plans dynamically
- Used max_length=512 for text generation
- Implemented error handling using try-except block
- Displayed user-friendly error messages

### 4️⃣ Deployment
- Created Hugging Face Space
- Selected Streamlit SDK
- Uploaded project files
- Added dependencies in requirements.txt
- Successfully deployed the application

---

## 🧪 Testing Scenarios

The model was tested with three different user scenarios:

### ✅ Scenario 1
- Fitness Level: Beginner  
- Goal: Weight Loss  
- Equipment: None  

Result: Generated safe bodyweight home workout plan.

---

### ✅ Scenario 2
- Fitness Level: Intermediate  
- Goal: Muscle Gain  
- Equipment: Dumbbells  

Result: Generated structured strength-based workout with sets and reps.

---

### ✅ Scenario 3
- Fitness Level: Advanced  
- Goal: Maintain Fitness  
- Equipment: Gym  

Result: Generated detailed gym routine including compound exercises.

Screenshots of these outputs are available in the screenshots/ folder.

---
## Hugging Face Space Link

Deployed Link ::https://huggingface.co/spaces/kethanakamireddy/module2

---


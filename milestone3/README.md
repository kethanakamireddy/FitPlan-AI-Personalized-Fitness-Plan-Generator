Milestone 3: Login System with OTP Verification
Overview

FitPlan AI is a web-based application that generates personalized fitness plans based on user inputs.
This milestone focuses on implementing a secure authentication system with database connectivity and OTP verification.

The system allows users to register, log in, verify their identity using a One-Time Password (OTP), and access the dashboard only after successful verification.

Key Features

User Signup with Email and Password

Secure Login Authentication

User Data Storage using SQLite Database

Automatic 6-digit OTP Generation after login

OTP Sent to Registered Email

OTP Verification Page

Dashboard Access after Successful OTP Validation

Technologies Used

Python

Streamlit

SQLite

SMTP / Email Services for OTP

GitHub

Hugging Face Spaces (Deployment)

Project Files :

app.py – Main Streamlit application that manages the user interface for signup, login, OTP verification, and dashboard access.

database.py – Handles all database operations such as creating the user table, storing user details, and validating login credentials.

auth.py – Generates and manages the OTP used for user authentication after login.

email_utils.py – Sends the generated OTP to the user’s registered email address.

requirements.txt – Lists all Python libraries required to run the project.

README.md – Provides project documentation including overview, features, setup instructions, and usage details.

How It Works

Users create an account using email and password.

User credentials are stored in a database.

After login, the system generates a 6-digit OTP.

The OTP is sent to the user's registered email.

The user enters the OTP for verification.

After successful verification, the user gains access to the dashboard.

Deployment

The application is deployed using Streamlit on Hugging Face Spaces.
Hugging Face Live Link:https://huggingface.co/spaces/kethanakamireddy/aifitnessloginpage


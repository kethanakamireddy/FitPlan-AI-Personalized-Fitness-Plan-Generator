import os
import requests
from dotenv import load_dotenv
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def send_otp_email(receiver_email, otp):
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [{
            "to": [{"email": receiver_email}]
        }],
        "from": {"email": SENDER_EMAIL},
        "subject": "Your FitPlan AI OTP",
        "content": [{
            "type": "text/plain",
            "value": f"Your OTP is: {otp}"
        }]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 202:
        raise Exception("Failed to send email")

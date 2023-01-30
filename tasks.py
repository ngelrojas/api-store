import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
api_key = os.getenv("MAILGUN_API_KEY")


def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", api_key),
        data={
            "from": f"info rednodes <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body
        }
    )


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "successfully signed up",
        f"hi {username}! you have successfully signed up to the stores rest api."
    )

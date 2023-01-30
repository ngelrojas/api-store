import os

import jinja2
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
api_key = os.getenv("MAILGUN_API_KEY")

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", api_key),
        data={
            "from": f"info rednodes <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html
        }
    )


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "successfully signed up",
        f"hi {username}! you have successfully signed up to the stores rest api.",
        render_template("email/action.html", username=username)
    )
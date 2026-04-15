import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL = os.getenv('EMAIL')

def send_email(subject, body, to):
    message = Mail(
        from_email=EMAIL,
        to_emails=to,
        subject=subject,
        plain_text_content=body
    )
    client = SendGridAPIClient(SENDGRID_API_KEY)
    client.send(message)

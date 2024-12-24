import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

# Replace with your Gmail email address
load_dotenv()
EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APPPASSWORD') # Use the 16-character App Password

def send_email(subject, body, to):
    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login with your email and the App Password
    server.login(EMAIL, APP_PASSWORD)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.sendmail(EMAIL, to, msg.as_string())

    # Close the server
    server.quit()

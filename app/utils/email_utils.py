import smtplib
from email.message import EmailMessage
import os

def send_credentials_email(email: str, password: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Admin/Writer Account Access"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = email
    msg.set_content(f"Welcome!\n\nYour account has been created.\n\nEmail: {email}\nTemporary Password: {password}\n\nPlease change your password after login.")

    with smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)

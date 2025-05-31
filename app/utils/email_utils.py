import smtplib
import socket
from email.message import EmailMessage
import os
import logging

logger = logging.getLogger(__name__)

def send_credentials_email(email: str, password: str):
    try:
        # Use direct IP address instead of hostname
        SMTP_IP = "142.251.32.109"  # smtp.gmail.com IP
        SMTP_PORT = 465
        
        msg = EmailMessage()
        msg["Subject"] = "Your Admin/Writer Account Access"
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = email
        msg.set_content(
            f"Welcome to Ensight!\n\n"
            f"Your admin account has been created:\n"
            f"Email: {email}\n"
            f"Temporary Password: {password}\n\n"
            "Please login and reset your password immediately:\n"
            "http://localhost:5173/login\n\n"
            "This is an automated message - please do not reply."
        )
        
        # Connect directly to IP
        with smtplib.SMTP_SSL(SMTP_IP, SMTP_PORT) as smtp:
            smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
            smtp.send_message(msg)
        
        logger.info(f"Credentials email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")
        return False
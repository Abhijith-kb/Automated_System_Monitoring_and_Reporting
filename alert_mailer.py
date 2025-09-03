# alert_mailer.py
import smtplib                              # Python’s built-in library to send emails using the SMTP protocol (what email servers use to talk to each other).
from email.message import EmailMessage      # A simple way to create and format emails.
from config import EMAIL_SETTINGS       

def send_alert(subject: str, body: str):
    msg = EmailMessage()                    # Creates a new empty email message.
    msg["Subject"] = subject                # Sets the email subject line (like the title of the email).
    msg["From"] = EMAIL_SETTINGS["from"]    # Sets the sender (your Gmail address).
    
    # Support single or multiple recipients
    recipients = EMAIL_SETTINGS["to"]
    if isinstance(recipients, list):
        msg["To"] = ", ".join(recipients)   # Adds all the recipient emails by joining them into one string (if you have multiple recipients).
    else:
        msg["To"] = recipients

    msg.set_content(body)

    try:
        with smtplib.SMTP(EMAIL_SETTINGS["server"], EMAIL_SETTINGS["port"]) as server:      # without using with, we have to server.quit() after sending.
            server.starttls()                                                               # Start secure connection
            server.login(EMAIL_SETTINGS["from"], EMAIL_SETTINGS["password"])
            server.send_message(msg)                                                        # cleaner than sendmail
        # print("✅ Alert email sent successfully")
    except Exception as e:
        print("❌ Failed to send email:", e)

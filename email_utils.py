import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())

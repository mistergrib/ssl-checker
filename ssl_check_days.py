import ssl
import socket
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
# Params, variables, etc
domains_env = os.getenv("HOSTNAMES")
domains = domains_env.split(",")
days_threshold = os.getenv("DAYS_THRESHOLD")
tg_alerts_enabled = bool(os.getenv("TELEGRAM_ALERTS_ENABLED").lower() == "true")
email_alerts_enabled = bool(os.getenv("EMAIL_ALERTS_ENABLED").lower() == "true")
tg_bot_token = os.getenv("BOT_TOKEN")
tg_group = os.getenv("CHAT_ID")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_STARTTLS_enabled = bool(os.getenv("SMTP_STARTTLS_ENABLED").lower() == "true")
smtp_SSL_enabled = bool(os.getenv("SMTP_SSL_ENABLED").lower() == "true")
email_login = os.getenv("EMAIL_LOGIN")
email_from_address = os.getenv("EMAIL_FROM_ADDRESSES")
email_password = os.getenv("EMAIL_PASSWORD")
email_subject = os.getenv("EMAIL_SUBJECT")
recipient_email = os.getenv("EMAIL_RECIPIENT")


def get_cert_expiry(hostname, port=443):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                return expiry_date
    except ssl.SSLCertVerificationError as e:
        print(f"Certificate was expired for {hostname}: {e}")
        return f"Certificate was expired for {hostname}: {e}"
    except ConnectionRefusedError as e:
        print(f"Can't connect to {hostname}: {e}")
        return f"Can't connect to {hostname}: {e}"
    except Exception as e:
        print(f"We got an error: {e}")
        return f"We got an error with {hostname}: {e}"


def send_tg_message(token, chat_id, alert):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': alert
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Message sent successfully:\n{full_message}")
        else:
            print(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")


def send_email(server, port):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_login
        msg['To'] = recipient_email
        msg['Subject'] = email_subject
        msg.attach(MIMEText(full_message, 'plain'))

        if smtp_STARTTLS_enabled and smtp_SSL_enabled:
            print("you should check one of the SMTP_STARTTLS_ENABLED or SMTP_SSL_ENABLED")
        try:
            if smtp_STARTTLS_enabled:
                smtp = smtplib.SMTP(server, port)
                smtp.starttls()
        except Exception as e:
            print(e)
        try:
            if smtp_SSL_enabled:
                smtp = smtplib.SMTP_SSL(server, port)
        except Exception as e:
            print(e)
        if not smtp_SSL_enabled and not smtp_STARTTLS_enabled:
            smtp = smtplib.SMTP(smtp_server, smtp_port)

        smtp.login(email_login, email_password)
        smtp.send_message(msg)

    except Exception as e:
        print(f"Can't send email: {e}")
    finally:
        smtp.quit()


full_message = ""
for domain in domains:
    today = datetime.utcnow()
    cert_date = get_cert_expiry(domain)
    if isinstance(cert_date, datetime):
        days_remaining = (cert_date - today).days
        if days_remaining <= int(days_threshold):
            message = f"{domain} expire in {days_remaining} days\n"
            full_message += message
    else:
        full_message = full_message + cert_date + "\n"


if tg_alerts_enabled:
    send_tg_message(tg_bot_token, tg_group, full_message)
if email_alerts_enabled:
    send_email(smtp_server, smtp_port)

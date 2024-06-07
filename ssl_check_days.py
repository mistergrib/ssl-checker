import ssl
import socket
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Params, variables, etc
domains_env = os.getenv("HOSTNAMES")
domains = domains_env.split(",")
days_threshold = os.getenv("DAYS_THRESHOLD")
tg_bot_token = os.getenv("BOT_TOKEN")
tg_group = os.getenv("CHAT_ID")


def get_cert_expiry(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            return expiry_date


def send_tg_message(token, chat_id, alert):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': alert
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message sent successfully")
            print(message)
        else:
            print(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")



for domain in domains:
    today = datetime.utcnow()
    days_remaining = (get_cert_expiry(domain) - today).days
    if days_remaining <= int(days_threshold):
        message = f"{domain} expire in {days_remaining} days"
        send_tg_message(tg_bot_token, tg_group, message)

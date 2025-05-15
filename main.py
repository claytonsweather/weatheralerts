import os
import requests
import json
import smtplib
from email.message import EmailMessage

# ==== Email Config ====
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECIPIENT = os.environ["EMAIL_RECIPIENT"]

# ==== GitHub Gist Config ====
GIST_ID = "cc77ca8c82ed2627b2ea5d57e4743efa"
GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
GIST_HEADERS = {
    "Authorization": f"token {os.environ['GIST_TOKEN']}"
}

# ==== Functions for Gist ====

def load_sent_alerts():
    """Load the list of alert IDs already sent from the Gist."""
    try:
        r = requests.get(GIST_URL, headers=GIST_HEADERS)
        r.raise_for_status()
        gist_data = r.json()
        file_content = gist_data['files']['sent_alerts.json']['content']
        return json.loads(file_content)
    except Exception as e:
        print(f"[ERROR] Could not load sent alerts: {e}")
        return []

def save_sent_alerts(alert_ids):
    """Save updated list of sent alert IDs to the Gist."""
    try:
        payload = {
            "files": {
                "sent_alerts.json": {
                    "content": json.dumps(alert_ids, indent=2)
                }
            }
        }
        r = requests.patch(GIST_URL, headers=GIST_HEADERS, json=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Could not save sent alerts: {e}")

# ==== Function to Send Email ====

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"[INFO] Sent: {subject}")

# ==== Get Alerts from NWS ====

def get_nws_alerts(area="TXZ213,TXZ214,TXZ215"):
    """Fetch active alerts for a comma-separated zone list (e.g., TXZ213)."""
    url = f"https://api.weather.gov/alerts/active?zone={area}"
    r = requests.get(url, headers={"User-Agent": "ClaytonWeatherBot"})
    r.raise_for_status()
    return r.json().get("features", [])

# ==== Main Logic ====

def main():
    sent_ids = load_sent_alerts()
    updated_ids = sent_ids.copy()
    alerts = get_nws_alerts()

    for alert in alerts:
        alert_id = alert["id"]
        if alert_id not in sent_ids:
            props = alert["properties"]
            subject = f"🚨 {props['event']} in {props['areaDesc']}"
            body = f"{props['headline']}\n\n{props['description']}\n\n{props['instruction']}"
            send_email(subject, body)
            updated_ids.append(alert_id)

    save_sent_alerts(updated_ids)

if __name__ == "__main__":
    main()

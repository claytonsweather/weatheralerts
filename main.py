import requests
import os
import json
from email_utils import send_email

# Config
GIST_ID = "cc77ca8c82ed2627b2ea5d57e4743efa"
GIST_FILENAME = "sent_alerts.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"
NWS_ALERTS_URL = "https://api.weather.gov/alerts/active"
MONITORED_LOCATIONS = [
    "new braunfels", "houston", "west columbia",
    "pearland", "lake jackson", "angleton", "clute"
]

HEADERS = {
    "Authorization": f"token {os.environ['GIST_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}

def load_sent_alerts():
    try:
        response = requests.get(GIST_API_URL, headers=HEADERS)
        response.raise_for_status()
        files = response.json()["files"]
        if GIST_FILENAME in files:
            content = files[GIST_FILENAME]["content"]
            return json.loads(content)
        else:
            print(f"⚠️ File {GIST_FILENAME} not found in the Gist.")
            return []
    except Exception as e:
        print(f"❌ Error loading sent alerts: {e}")
        return []

def save_sent_alerts(alert_ids):
    try:
        updated_file = {
            "files": {
                GIST_FILENAME: {
                    "content": json.dumps(alert_ids, indent=2)
                }
            }
        }
        response = requests.patch(GIST_API_URL, headers=HEADERS, json=updated_file)
        response.raise_for_status()
        print("✅ Sent alerts saved to Gist.")
    except Exception as e:
        print(f"❌ Error saving sent alerts: {e}")

def fetch_nws_alerts():
    try:
        response = requests.get(NWS_ALERTS_URL)
        response.raise_for_status()
        return response.json()["features"]
    except Exception as e:
        print(f"❌ Error fetching NWS alerts: {e}")
        return []

def is_for_monitored_location(area_desc):
    area = area_desc.lower()
    return any(loc in area for loc in MONITORED_LOCATIONS)

def main():
    sent_alerts = load_sent_alerts()
    alerts = fetch_nws_alerts()
    new_alerts_sent = 0

    for alert in alerts:
        props = alert["properties"]
        area_desc = props.get("areaDesc", "")
        if not is_for_monitored_location(area_desc):
            continue

        alert_id = alert["id"]
        if alert_id in sent_alerts:
            continue

        title = props.get("headline", "⚠️ Weather Alert")
        description = props.get("description", "No description provided.")
        instruction = props.get("instruction", "")

        alert_msg = f"{title}\n\nArea: {area_desc}\n\n{description}\n\n{instruction}"
        send_email(f"🌩️ {title}", alert_msg)

        sent_alerts.append(alert_id)
        new_alerts_sent += 1

    if new_alerts_sent:
        save_sent_alerts(sent_alerts)
    else:
        print("✅ No new alerts to send.")

if __name__ == "__main__":
    main()

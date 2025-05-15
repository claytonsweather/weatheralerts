import requests
import os
import json
from email_utils import send_email

GIST_ID = "cc77ca8c82ed2627b2ea5d57e4743efa"
GIST_FILENAME = "sent_alerts.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

HEADERS = {
    "Authorization": f"token {os.environ['GIST_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}

# Modify this to filter by your region if needed
NWS_ALERTS_URL = "https://api.weather.gov/alerts/active?area=TX"

def load_sent_alerts():
    try:
        response = requests.get(GIST_API_URL, headers=HEADERS)
        response.raise_for_status()
        files = response.json()["files"]
        if GIST_FILENAME in files:
            content = files[GIST_FILENAME]["content"]
            return json.loads(content)
        else:
            print(f"File {GIST_FILENAME} not found in the Gist.")
            return []
    except Exception as e:
        print(f"Error loading sent alerts: {e}")
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
        print("✅ Sent alerts saved successfully.")
    except Exception as e:
        print(f"Error saving sent alerts: {e}")

def fetch_nws_alerts():
    try:
        response = requests.get(NWS_ALERTS_URL)
        response.raise_for_status()
        return response.json()["features"]
    except Exception as

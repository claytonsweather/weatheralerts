import os
import json
import requests

GIST_ID = "cc77ca8c82ed2627b2ea5d57e4743efa"
FILENAME = "sent_alerts.json"

def get_headers():
    return {
        "Authorization": f"token {os.environ['GIST_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }

def load_sent_alerts():
    try:
        response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=get_headers())
        response.raise_for_status()
        files = response.json().get("files", {})
        content = files.get(FILENAME, {}).get("content", "[]")
        return set(json.loads(content))
    except Exception as e:
        print(f"Error:  Could not load sent alerts: {e}")
        return set()

def save_sent_alerts(alert_ids):
    try:
        data = {
            "files": {
                FILENAME: {
                    "content": json.dumps(list(alert_ids), indent=2)
                }
            }
        }
        response = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=get_headers(), json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error:  Could not save sent alerts: {e}")

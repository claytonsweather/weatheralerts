import os
import sys
import requests
from email_utils import send_email
from gist_utils import load_sent_alerts, save_sent_alerts

# NWS Zone Codes for your Texas locations
ZONE_CODES = [
    "TXZ213",  # Houston
    "TXZ226",  # West Columbia
    "TXZ227",  # Lake Jackson
    "TXZ228",  # Angleton / Clute
    "TXZ237",  # Pearland
    "TXZ209",  # New Braunfels
]

def fetch_alerts(zone_code):
    url = f"https://api.weather.gov/alerts/active/zone/{zone_code}"
    headers = {"User-Agent": "ClaytonWeatherAlerts/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("features", [])
    except Exception as e:
        print(f"⚠️ Error fetching alerts for {zone_code}: {e}")
        return []

def format_alert(alert):
    props = alert["properties"]
    return f"""
⚠️ **{props.get('event', 'Unknown Event')}**
{props.get('headline', '')}

{props.get('description', '').strip()}

🚨 **Effective:** {props.get('effective')}
🕔 **Expires:** {props.get('expires')}

🔗 {props.get('uri')}
""".strip()

def main():
    test_mode = '--test' in sys.argv
    if test_mode:
        send_email("✅ Test Alert", "This is a test of the weather alert system.")
        print("✅ Test alert sent.")
        return

    sent_alerts = load_sent_alerts() or set()
    new_alerts = []
    new_ids = set()

    for zone in ZONE_CODES:
        alerts = fetch_alerts(zone)
        for alert in alerts:
            alert_id = alert["id"]
            if alert_id not in sent_alerts:
                print(f"📬 New alert found: {alert_id}")
                new_alerts.append(alert)
                new_ids.add(alert_id)

    for alert in new_alerts:
        message = format_alert(alert)
        title = alert["properties"].get("event", "Weather Alert")
        send_email(f"🌩️ {title}", message)

    if new_ids:
        sent_alerts.update(new_ids)
        save_sent_alerts(sent_alerts)

if __name__ == "__main__":
    main()


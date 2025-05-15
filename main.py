import os
import requests
import json
from alert_utils import get_alerts, filter_alerts, format_alert
from email_utils import send_email

def main():
    alerts = get_alerts()
    matched = filter_alerts(alerts)
    
    for loc, alert in matched:
        message = format_alert(loc, alert)
        subject = f"🚨 Alert for {loc}: {alert['properties']['event']}"
        send_email(subject, message)

if __name__ == "__main__":
    main()

import requests
from config import LOCATIONS

def get_alerts():
    url = "https://api.weather.gov/alerts/active"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data.get("features", [])

def filter_alerts(alerts):
    matched = []
    for alert in alerts:
        area = alert["properties"]["areaDesc"].lower()
        for loc in LOCATIONS:
            if loc.lower() in area:
                matched.append((loc, alert))
    return matched

def format_alert(loc, alert):
    props = alert["properties"]
    return f"""⚠️ WEATHER ALERT for {loc.upper()} ⚠️

{props['headline']}

{props['description']}

Instructions: {props.get('instruction', 'N/A')}
Expires: {props['expires']}
"""

# Weather Alert Email System

This project automatically checks for active weather alerts from the National Weather Service (NWS) and emails them to a specified recipient list — perfect for sending real-time alerts to a Notify.Events address or personal inbox.

## 🔧 Features

- Pulls active alerts from the [NWS API](https://api.weather.gov/alerts/active)
- Filters alerts by specific location names
- Sends formatted weather alerts via email
- Easy to customize and extend
- Ready for automation with cron or Task Scheduler

---

## 📦 Requirements

- Python 3.7+
- Internet connection
- Gmail account (or SMTP-capable email service)
- Python packages (installed below)

---

## 🚀 Setup

1. **Clone or Download** this repository.

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt

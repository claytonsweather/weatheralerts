import os

EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECIPIENTS = [os.environ["EMAIL_RECIPIENT"]]

LOCATIONS = [
    "Houston", "Angleton", "West Columbia", "Huntsville",
    "Crystal City", "Rocksprings", "New Braunfels"
]

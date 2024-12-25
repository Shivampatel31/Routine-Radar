import logging
from plyer import notification
from datetime import datetime, timezone, timedelta
from time import sleep
import winsound  # For sound notifications

# Set up logging to track when reminders are sent. It will log all reminders in a text file.
logging.basicConfig(filename='reminder_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')


# Function to play a sound when a reminder is triggered.
# This will use the system speaker to play a simple beep sound.
def play_sound():
    winsound.Beep(1000, 1000)  # Frequency 1000 Hz, duration 1000 ms


# List of one-time reminders with specific times (e.g., lunch, snacks, sleep)
reminders = [
    {"time": "13:00", "message": "It's time for lunch and water!!"},  # Reminder for lunch
    {"time": "16:00", "message": "It's time for snacks and water!!"},  # Reminder for snacks
    {"time": "18:00", "message": "It's time to log off from work!!"},  # Reminder to log off work
    {"time": "23:30", "message": "It's time to sleep, get some rest!!"}  # Reminder to sleep
]

# List of recurring reminders for water every hour between 9 AM and 10 PM
# These reminders will repeat every day to remind the user to drink water.
recurring_tasks = [
    {"time": "09:00", "message": "It's time to drink water!!"},
    {"time": "10:00", "message": "It's time to drink water!!"},
    {"time": "11:00", "message": "It's time to drink water!!"},
    {"time": "12:00", "message": "It's time to drink water!!"},
    {"time": "14:00", "message": "It's time to drink water!!"},
    {"time": "15:00", "message": "It's time to drink water!!"},
    {"time": "17:00", "message": "It's time to drink water!!"},
    {"time": "19:00", "message": "It's time to drink water!!"},
    {"time": "20:00", "message": "It's time to drink water!!"},
    {"time": "21:00", "message": "It's time to drink water!!"},
    {"time": "22:00", "message": "It's time to drink water!!"}
]

# Combine both one-time reminders and recurring tasks into a single list
# This simplifies the reminder check and makes the code more efficient
all_reminders = reminders + recurring_tasks

# Dictionary to track if notifications for each reminder have been sent today.
# Keys are the reminder times, values are booleans to indicate if the reminder has been sent.
is_notification_sent = {reminder["time"]: False for reminder in all_reminders}


# Function to send notifications with both visual alert and sound
def send_reminder(msg):
    # Use plyer's notification module to show a notification with the provided message
    notification.notify(
        title="Urgent Reminder",  # Title of the notification
        message=msg,  # Message content to be displayed in the notification
        timeout=5  # The notification will stay visible for 5 seconds
    )
    # Play a sound as an additional alert for the user
    play_sound()
    # Log this reminder in a text file for record-keeping
    logging.info(f"Sent reminder: {msg}")


# Function to check the time and send the corresponding reminders
def schedule(date):
    # Convert the current time to the format HH:MM (24-hour format)
    current_time = date.strftime("%H:%M")

    # Loop through all reminders (both one-time and recurring)
    for reminder in all_reminders:
        # Check if the current time matches any of the scheduled reminder times
        # and if the reminder hasn't been sent already today
        if current_time == reminder["time"] and not is_notification_sent[reminder["time"]]:
            # Mark the reminder as sent
            is_notification_sent[reminder["time"]] = True
            # Send the reminder
            send_reminder(reminder["message"])


# Function to reset reminders at the start of a new day
def reset_notifications(date, prev_date):
    # If it's a new day (based on the day change), reset all reminders for the new day
    if date.day == 1 or date.day > prev_date.day:
        global is_notification_sent
        # Set all reminders' sent status to False to enable notifications for the new day
        is_notification_sent = {reminder["time"]: False for reminder in all_reminders}
        prev_date = date  # Update the previous date to the current one
    return prev_date


# Main program execution
if __name__ == "__main__":
    # Initialize previous date to be one day before the current date to ensure the first reset
    prev_date = datetime.now(timezone.utc) - timedelta(days=1)

    # Start an infinite loop to continuously check the time and send reminders
    while True:
        # Get the current time in UTC and convert it to the local timezone
        date = datetime.now(timezone.utc).astimezone()

        # Reset notifications if the day has changed (i.e., it's a new day)
        prev_date = reset_notifications(date, prev_date)

        # Check and send relevant reminders based on the current time
        schedule(date)

        # Sleep for 5 minutes (300 seconds) before checking the time again
        # This reduces the load on the system while checking for reminders periodically
        sleep(300)

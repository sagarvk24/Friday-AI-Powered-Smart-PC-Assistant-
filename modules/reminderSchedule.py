import datetime
import threading
from textToSpeech import TextToSpeech

tts = TextToSpeech(mode="offline")

class ReminderManager:
    def __init__(self):
        self.reminders = []

    def set_reminder(self, task, time_string):
        try:
            now = datetime.datetime.now()
            reminder_time = datetime.datetime.strptime(time_string, "%I %p")  # "4 PM"
            reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)

            if reminder_time < now:
                reminder_time += datetime.timedelta(days=1)  # next day if time passed

            delay = (reminder_time - now).total_seconds()

            # Store it
            self.reminders.append({"task": task, "time": reminder_time.strftime("%I:%M %p")})

            # Schedule it
            threading.Timer(delay, self._trigger_reminder, args=[task]).start()
            return f"⏰ Okay User, I’ll remind you to {task} at {reminder_time.strftime('%I:%M %p')}."
        except Exception as e:
            return f"Sorry User, I couldn’t set that reminder. Error: {e}"

    def _trigger_reminder(self, task):
        tts.speak(f"Hey User, it’s time to {task} 💡")

if __name__ == "__main__":
    rm = ReminderManager()
    print(rm.set_reminder("drink water", "4 PM"))

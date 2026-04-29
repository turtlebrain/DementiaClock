from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import init_db, get_next_reminder, get_pending_reminders, add_reminder, log_button_press, mark_reminder_notified
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pyttsx3


app = Flask(__name__)
scheduler = BackgroundScheduler()


def notify_reminder(reminder_id, title, time_label):
    message = f"Reminder in 10 minutes: {title} at {time_label}"
    print(f"Reminder triggered: {message}")
    speak(message)
    mark_reminder_notified(reminder_id)


def schedule_reminder_notification(reminder):
    reminder_time = datetime.fromisoformat(reminder["timestamp"])
    fire_at = reminder_time - timedelta(minutes=10)

    scheduler.add_job(
        notify_reminder,
        trigger="date",
        run_date=fire_at,
        args=[reminder["id"], reminder["title"], reminder["time"]],
        id=f"reminder_{reminder['id']}",
        replace_existing=True
    )


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/api/next-reminder")
def api_next_reminder():
    reminder = get_next_reminder()

    if reminder is None:
        return jsonify({"message": "no reminders"}), 200

    return jsonify(reminder)


@app.route("/dashboard")
def dashboard():
    # For now, we only show the form — listing reminders comes later
    return render_template("dashboard.html")


@app.route("/add-reminder", methods=["POST"])
def add_reminder_route():
    title = request.form.get("title")
    time = request.form.get("time")
    timestamp = request.form.get("timestamp")

    add_reminder(title, time, timestamp)
    reminder = get_next_reminder()
    if reminder and reminder["title"] == title and reminder["timestamp"] == timestamp:
        schedule_reminder_notification(reminder)

    return redirect(url_for("dashboard"))


@app.route("/api/test-press", methods=["POST"])
def api_test_press():
    press_type = request.json.get("type", "short_press")
    log_button_press(press_type)
    reminder = get_next_reminder()
    if reminder:
        speak(f"Your next reminder is {reminder['title']} at {reminder['time']}")
    else:
        speak("You have no reminders scheduled")
    return jsonify({"status": "ok"})


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def main():
    init_db()

    global tts_engine
    tts_engine = pyttsx3.init()

    scheduler.start()

    for reminder in get_pending_reminders():
        schedule_reminder_notification(reminder)

    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    main()

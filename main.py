from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import init_db, get_next_reminder, add_reminder, log_button_press
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from db import get_next_reminder
import pyttsx3


app = Flask(__name__)

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

def check_reminders():
    reminder = get_next_reminder()
    if reminder is None:
        return

    now = datetime.now().isoformat(timespec="seconds")

    if reminder["timestamp"] <= now:
        message = f"It's time to {reminder['title']}"
        print(f"Reminder triggered: {message}")
        speak(message)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    init_db()

    global tts_engine
    tts_engine = pyttsx3.init()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_reminders,
        "interval",
        seconds=60,
        max_instances=1,
        coalesce=True
    )
    scheduler.start()

    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
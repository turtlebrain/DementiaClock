from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import init_db, get_next_reminder, add_reminder
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from db import get_next_reminder


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

def check_reminders():
    reminder = get_next_reminder()
    if reminder is None:
        return

    now = datetime.now().isoformat(timespec="seconds")

    # If the reminder timestamp is in the past or now, trigger it
    if reminder["timestamp"] <= now:
        print(f"Reminder triggered: {reminder['title']} at {reminder['time']}")
        # Later: TTS, UI highlight, logging, etc.


def main():
    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_reminders, "interval", seconds=30)
    scheduler.start()

    app.run(debug=True)

if __name__ == '__main__':
    main()
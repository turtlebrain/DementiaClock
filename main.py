from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/next-reminder")
def api_next_reminder():
    # Placeholder data — will come from a database later
    reminder = {
        "title": "Take medication",
        "time": "20:00",
        "timestamp": "2026-04-25T20:00:00"
    }
    return jsonify(reminder)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

# load .env
load_dotenv(override=True) # Reload env vars


# Import your installed package (installed as ai-helpers-meena -> module ai_helpers_meena)
from ai_helpers_meena.client import AIClient

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")  # for flash messages in dev

# Create client (it should read API key from env or you can pass explicitly)
client = AIClient(api_key=os.environ.get("GOOGLE_API_KEY"))

import json

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(hist):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(hist, f)
    except Exception as e:
        print(f"Error saving history: {e}")

# Load history on startup
history = load_history()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            flash("Please enter a prompt.", "warning")
            return redirect(url_for("index"))

        try:
            # 1) get raw response from AI
            raw = client.get_response(prompt)

            # 2) summarize optionally (example) — commented out but available
            # summary = client.summarize_text(raw)

            # 3) format for display
            out = client.format_response(raw)
            print(f"DEBUG: Prompt='{prompt}', Response='{out}'")

            # store in history
            history.insert(0, {"prompt": prompt, "response": out})
            print(f"DEBUG: History count={len(history)}")
            
            # keep history reasonably small
            if len(history) > 50:
                history.pop()
            
            save_history(history)

            return render_template("index.html", response=out, history=history)
        except Exception as e:
            # Graceful error handling
            flash(f"Error while calling AI: {e}", "danger")
            return redirect(url_for("index"))

    return render_template("index.html", history=history)

if __name__ == "__main__":
    # dev server
    app.run(host="127.0.0.1", port=5000, debug=True)

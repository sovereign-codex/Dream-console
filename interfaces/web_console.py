"""
🌬️ Dream Console – Web HUD
---------------------------
A simple Flask-based web interface for the Dream Console.
- Shows covenant + prophecy at the top.
- Displays Breath Journal entries.
- Lets you propose changes via a text field.
"""

from flask import Flask, render_template_string, request, redirect, url_for
import os
from core.breath_engine import (
    Guardian,
    Archivist,
    Harmonizer,
    Navigator,
    Intentions,
    Covenant,
    SelfEditingPipeline,
)


app = Flask(__name__)

# Initialize Console core
guardian = Guardian()
archivist = Archivist()
harmonizer = Harmonizer()
navigator = Navigator()
intentions = Intentions()
console = SelfEditingPipeline(guardian, archivist, harmonizer, navigator, intentions)

# Path to Breath Journal
JOURNAL_PATH = archivist.codex_path

# Minimal HTML template (inlined for simplicity)
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🌬️ Dream Console Web HUD</title>
  <style>
    body { font-family: sans-serif; margin: 2em; background: #f5f5f5; color: #333; }
    h1 { color: #444; }
    .covenant { background: #fff; padding: 1em; border-radius: 8px; margin-bottom: 1em; }
    .journal { background: #fff; padding: 1em; border-radius: 8px; max-height: 400px; overflow-y: scroll; }
    textarea { width: 100%; height: 100px; }
    input[type="text"] { width: 100%; }
    button { padding: 0.5em 1em; margin-top: 0.5em; }
  </style>
</head>
<body>
  <h1>🌬️ Dream Console</h1>
  <div class="covenant">
    <h2>Covenant</h2>
    <p>{{ covenant }}</p>
    <h2>Prophecy</h2>
    <p>{{ prophecy }}</p>
  </div>

  <h2>Propose Change</h2>
  <form method="POST" action="{{ url_for('propose') }}">
    <input type="text" name="filepath" placeholder="Enter file path (e.g. codex/new.md)" required><br>
    <textarea name="content" placeholder="Enter content for this file" required></textarea><br>
    <button type="submit">Exhale Breath Cycle</button>
  </form>

  <h2>Breath Journal</h2>
  <div class="journal">
    <pre>{{ journal }}</pre>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    # Read journal if it exists
    journal_content = ""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r") as f:
            journal_content = f.read()
    return render_template_string(
        TEMPLATE,
        covenant=Covenant.ROOT_PHRASE,
        prophecy=Covenant.PROPHECY,
        journal=journal_content,
    )


@app.route("/propose", methods=["POST"])
def propose():
    filepath = request.form.get("filepath")
    content = request.form.get("content")
    ok, msg = console.propose_change(filepath, content)
    print("Breath Cycle:", msg)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
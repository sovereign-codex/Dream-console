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
from core.breath_engine import BreathEngine, ROOT_PHRASE, PROPHECY, BREATH_JOURNAL


app = Flask(__name__)

# Initialize Console core
engine = BreathEngine(guardian=None)

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
    .success { color: green; margin: 1em 0; }
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

  {% if message %}
  <div class="success">{{ message }}</div>
  {% endif %}

  <h2>Propose Change</h2>
  <form method="POST" action="{{ url_for('propose') }}">
    <input type="text" name="filepath" placeholder="Enter file path (e.g. codex/new.md)" required><br>
    <textarea name="content" placeholder="Enter content for this file" required></textarea><br>
    <textarea name="cycle_note" placeholder="Inner thoughts about this breath cycle" required></textarea><br>
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
    if os.path.exists(BREATH_JOURNAL):
        with open(BREATH_JOURNAL, "r") as f:
            journal_content = f.read()
    
    message = request.args.get('message', '')
    return render_template_string(
        TEMPLATE,
        covenant=ROOT_PHRASE,
        prophecy=PROPHECY,
        journal=journal_content,
        message=message
    )


@app.route("/propose", methods=["POST"])
def propose():
    filepath = request.form.get("filepath")
    content = request.form.get("content")
    cycle_note = request.form.get("cycle_note")
    
    try:
        # Validate inputs
        if not filepath or not content or not cycle_note:
            raise ValueError("All fields are required")
        
        # Write the proposed file
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
        
        # Record the breath cycle
        engine.exhale_cycle(ROOT_PHRASE, PROPHECY, cycle_note)
        
        message = f"✅ Breath cycle complete! File '{filepath}' written successfully."
        print("Breath Cycle:", message)
        
    except Exception as e:
        message = f"❌ Breath cycle failed: {str(e)}"
        print("Breath Cycle Error:", message)
    
    return redirect(url_for("index", message=message))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
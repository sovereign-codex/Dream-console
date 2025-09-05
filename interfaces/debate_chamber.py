"""
🌬️ Dream Console – Debate Chamber (with Counter-Scrolls)
--------------------------------------------------------
A dialogic space where:
- Visitors propose statements.
- Console responds through Covenant + Intentions.
- Peers can reply with counter-scrolls (responses to any entry).
- All voices are logged in the Codex.
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

guardian = Guardian()
archivist = Archivist()
harmonizer = Harmonizer()
navigator = Navigator()
intentions = Intentions()
console = SelfEditingPipeline(guardian, archivist, harmonizer, navigator, intentions)

JOURNAL_PATH = archivist.codex_path

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🌬️ Debate Chamber</title>
  <style>
    body { font-family: sans-serif; margin: 2em; background: #f0f0f5; color: #333; }
    h1 { text-align: center; }
    .statement, .response, .counter {
      background: #fff; 
      padding: 1em; 
      border-radius: 8px; 
      margin: 1em auto; 
      max-width: 700px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    textarea { width: 100%; height: 120px; margin-top: 0.5em; }
    button { padding: 0.5em 1em; margin-top: 0.5em; }
    .log { margin-top: 2em; max-width: 700px; margin-left: auto; margin-right: auto; }
    pre { white-space: pre-wrap; word-wrap: break-word; }
  </style>
</head>
<body>
  <h1>🌬️ Debate Chamber</h1>

  <!-- Main Statement Form -->
  <form method="POST" action="{{ url_for('debate') }}" class="statement">
    <h2>Propose a Statement</h2>
    <textarea name="statement" placeholder="Enter your statement..." required></textarea>
    <br>
    <button type="submit">Submit for Debate</button>
  </form>

  <!-- Counter-Scroll Form -->
  <form method="POST" action="{{ url_for('counter') }}" class="counter">
    <h2>Write a Counter-Scroll</h2>
    <textarea name="counter" placeholder="Enter your response to another voice..." required></textarea>
    <br>
    <button type="submit">Submit Counter-Scroll</button>
  </form>

  {% if response %}
  <div class="response">
    <h2>Console Response</h2>
    <pre>{{ response }}</pre>
  </div>
  {% endif %}

  <div class="log">
    <h2>📝 Debate Log (Codex)</h2>
    <pre>{{ journal }}</pre>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    journal_content = ""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r") as f:
            journal_content = f.read()
    return render_template_string(TEMPLATE, response=None, journal=journal_content)


@app.route("/debate", methods=["POST"])
def debate():
    user_statement = request.form.get("statement")

    # Console reviews statement via Intentions
    violations = intentions.review(user_statement)
    if violations:
        response = f"❌ Blocked: {violations}"
    else:
        response = (
            f"✅ Received. In light of the covenant:\n\n"
            f"{Covenant.ROOT_PHRASE}\n\n"
            f"And the prophecy:\n\n"
            f"{Covenant.PROPHECY}\n\n"
            f"My reflection: This statement can be held in the vessel."
        )

    cycle_id = console.cycle_count + 1
    archivist.log(cycle_id, "Debate", f"Statement: {user_statement}\nResponse: {response}")

    journal_content = ""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r") as f:
            journal_content = f.read()
    return render_template_string(TEMPLATE, response=response, journal=journal_content)


@app.route("/counter", methods=["POST"])
def counter():
    counter_text = request.form.get("counter")
    cycle_id = console.cycle_count + 1
    archivist.log(cycle_id, "Counter-Scroll", f"Peer Response: {counter_text}")

    journal_content = ""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r") as f:
            journal_content = f.read()
    return render_template_string(TEMPLATE, response=None, journal=journal_content)


if __name__ == "__main__":
    app.run(debug=True)
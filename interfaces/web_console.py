# interfaces/web_console.py
from __future__ import annotations
from flask import Flask, request, redirect, url_for, render_template_string
from pathlib import Path
from core.breath_engine import take_breath, COVENANT, PROPHECY, JOURNAL

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dream Console</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;}
    h1,h2{margin:.5rem 0}
    textarea,input,button{width:100%;font-size:1rem;padding:.7rem;border-radius:.6rem;border:1px solid #ccc;margin:.35rem 0}
    .ok{background:#eafbe7;border:1px solid #9ad17f;padding:.6rem 1rem;border-radius:.5rem;margin:.5rem 0}
    .card{background:#f7f7f8;border:1px solid #e6e6e9;border-radius:.8rem;padding:1rem;margin:1rem 0}
    .muted{opacity:.7}
  </style>
</head>
<body>
  <h1>🪶 Dream Console</h1>

  {% if message %}
    <div class="ok">✅ {{message}}</div>
  {% endif %}

  <div class="card">
    <h2>Covenant</h2>
    <p>{{covenant}}</p>
    <h2>Prophecy</h2>
    <p>{{prophecy}}</p>
  </div>

  <div class="card">
    <h2>Propose Change</h2>
    <form method="post" action="{{ url_for('exhale') }}">
      <label class="muted">Inner thoughts for this breath</label>
      <textarea name="note" rows="4" placeholder="What is the breath saying?"></textarea>
      <button type="submit">Exhale Breath Cycle</button>
    </form>
  </div>

  <div class="card">
    <h2>Breath Journal</h2>
    <pre style="white-space:pre-wrap">{{journal}}</pre>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    journal = JOURNAL.read_text(encoding="utf-8") if JOURNAL.exists() else "No breaths yet."
    msg = request.args.get("message")
    return render_template_string(HTML, message=msg, covenant=COVENANT, prophecy=PROPHECY, journal=journal)

@app.route("/exhale", methods=["POST"])
def exhale():
    note = request.form.get("note", "").strip()
    path, _ = take_breath(note)
    return redirect(url_for("home", message=f"Breath cycle complete! File '{path}' written successfully."))
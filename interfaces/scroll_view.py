"""
🌬️ Dream Console – Contemplative Scroll View
--------------------------------------------
This page renders Codex entries like a living scroll:
- Smooth, contemplative reading.
- Each cycle appears in order, like unrolling parchment.
"""

from flask import Flask, render_template_string
import os


JOURNAL_PATH = "codex/breath_journal.md"

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🌬️ Contemplative Scroll</title>
  <style>
    body { 
      font-family: 'Georgia', serif; 
      background: #fdfcf7; 
      color: #3a2f2f; 
      margin: 2em; 
      line-height: 1.6; 
    }
    h1, h2 { text-align: center; }
    .scroll {
      max-width: 700px;
      margin: auto;
      padding: 2em;
      background: #fffdfa;
      border: 1px solid #e5d9c6;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      overflow-y: auto;
      max-height: 80vh;
    }
    pre { white-space: pre-wrap; word-wrap: break-word; }
  </style>
</head>
<body>
  <h1>🌬️ The Living Codex</h1>
  <h2>Contemplative Scroll View</h2>
  <div class="scroll">
    <pre>{{ journal }}</pre>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    journal_content = ""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r") as f:
            journal_content = f.read()
    return render_template_string(TEMPLATE, journal=journal_content)


if __name__ == "__main__":
    app.run(debug=True)
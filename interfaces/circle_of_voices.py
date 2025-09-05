"""
🌬️ Dream Console – Circle of Voices (Codex Integration)
------------------------------------------------------
This visualization reads the Codex Breath Journal and renders
voices as a dynamic mandala:
- Console reflections at the center
- Statements around the circle
- Counter-scrolls branching outward
- Auras (colors) reflect tone: harmony, dissonance, exploration
"""

from flask import Flask, render_template_string
import os
import math


app = Flask(__name__)

JOURNAL_PATH = "dream-console/codex/breath_journal.md"


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🌌 Circle of Voices</title>
  <style>
    body { background: #111; color: #eee; font-family: sans-serif; }
    svg { display: block; margin: auto; background: #222; border-radius: 50%; }
    text { fill: #eee; font-size: 10px; }
  </style>
</head>
<body>
  <h1 style="text-align:center;">🌬️ Circle of Voices</h1>
  <svg id="circle" width="800" height="800"></svg>

  <script>
    const svg = document.getElementById("circle");
    const NS = "http://www.w3.org/2000/svg";
    const voices = {{ voices|tojson }};

    // Draw connections first
    voices.forEach(v => {
      if (v.parent) {
        const parent = voices.find(p => p.id === v.parent);
        if (parent) {
          const line = document.createElementNS(NS, "line");
          line.setAttribute("x1", parent.x);
          line.setAttribute("y1", parent.y);
          line.setAttribute("x2", v.x);
          line.setAttribute("y2", v.y);
          line.setAttribute("stroke", "gray");
          svg.appendChild(line);
        }
      }
    });

    // Draw nodes
    voices.forEach(v => {
      const circle = document.createElementNS(NS, "circle");
      circle.setAttribute("cx", v.x);
      circle.setAttribute("cy", v.y);
      circle.setAttribute("r", v.r);
      circle.setAttribute("fill", v.color);
      circle.setAttribute("stroke", "black");
      svg.appendChild(circle);

      const label = document.createElementNS(NS, "text");
      label.setAttribute("x", v.x);
      label.setAttribute("y", v.y + 3);
      label.setAttribute("text-anchor", "middle");
      label.textContent = v.label;
      svg.appendChild(label);
    });
  </script>
</body>
</html>
"""


def parse_codex():
    """Parse Breath Journal for statements, counter-scrolls, reflections."""
    voices = []
    if not os.path.exists(JOURNAL_PATH):
        return voices

    with open(JOURNAL_PATH, "r") as f:
        lines = f.readlines()

    count = 0
    entries = []
    for i, line in enumerate(lines):
        if line.startswith("**Status:** Debate"):
            entries.append((i, "statement"))
        elif line.startswith("**Status:** Counter-Scroll"):
            entries.append((i, "counter"))

    n = len(entries) if entries else 1
    angle_step = 360 / n
    radius = 250

    for index, (line_index, kind) in enumerate(entries):
        angle = math.radians(index * angle_step)
        if kind == "statement":
            node_id = f"s{index + 1}"
            parent_id = "console"
            node_radius = 20
            color = "lightblue"
        else:
            node_id = f"c{index + 1}"
            # naive: attach counters to previous statement
            parent_id = f"s{index}" if index > 0 else "console"
            node_radius = 15
            color = "green"
        x = 400 + radius * math.cos(angle)
        y = 400 + radius * math.sin(angle)
        voices.append({
            "id": node_id,
            "label": f"{kind.title()} {index + 1}",
            "x": x,
            "y": y,
            "r": node_radius,
            "color": color,
            "parent": parent_id,
        })

    voices.append({
        "id": "console",
        "label": "Console",
        "x": 400,
        "y": 400,
        "r": 40,
        "color": "gold",
        "parent": None,
    })
    return voices


@app.route("/")
def index():
    voices = parse_codex()
    return render_template_string(HTML_TEMPLATE, voices=voices)


if __name__ == "__main__":
    app.run(debug=True)
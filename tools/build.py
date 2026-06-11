#!/usr/bin/env python3
"""Injects validated data into index.template.html -> index.html.

Refuses to build unless the grounding validator passes first, so the
shipped app can never contain unvalidated evidence.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Gate: validator must pass before any build.
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_quotes.py")])
if r.returncode != 0:
    sys.exit("Build blocked: grounding validation failed.")

# short_name is the human label shown on the evidence-map chips (Amendment B);
# the rubric here is the single source of truth — never hard-code it in the template.
RUBRIC = [
    {"id": "S1", "name": "Builder Evidence", "short_name": "Builder",
     "definition": "Makes real things, not descriptions of things — code, configuration, low-code, APIs, orchestration; tests and hardens what was built."},
    {"id": "S2", "name": "Workflow & Systems Thinking", "short_name": "Workflow",
     "definition": "Designs multi-step processes around the model: human-AI handoffs, decision boundaries, deliberate autonomy levels, failure paths."},
    {"id": "S3", "name": "End-to-End Ownership", "short_name": "Ownership",
     "definition": "Carries a problem from definition to a working system people actually use — deployment, adoption, maintenance included."},
    {"id": "S4", "name": "Ambiguity → Direction", "short_name": "Ambiguity",
     "definition": "Enters undefined problems, makes explicit assumptions, commits to a scoped direction, tests and iterates."},
    {"id": "S5", "name": "Responsible AI Judgment", "short_name": "Responsible AI",
     "definition": "Treats risk, governance, ethics and trust as design constraints; evaluates AI behavior rather than only shipping it."},
    {"id": "S6", "name": "Enterprise Fluency & Value Targeting", "short_name": "Enterprise Value",
     "definition": "Understands how organizations operate; aims AI at pain points with tangible value; names stakeholders and constraints."},
]

LABELS = {"ENG-01": ("Candidate A", "engineer · repo README"),
          "CON-02": ("Candidate B", "consultant · results memo"),
          "STB-03": ("Candidate C", "self-taught · portfolio narrative")}

candidates = []
for cid, (label, fmt) in LABELS.items():
    source = (ROOT / "data" / "candidates" / f"{cid}.md").read_text(encoding="utf-8")
    extraction = json.loads((ROOT / "data" / "extractions" / f"{cid}.json").read_text(encoding="utf-8"))
    candidates.append({"id": cid, "label": label, "format": fmt,
                       "source": source, "extraction": extraction})

data = {"rubric": RUBRIC, "candidates": candidates}
payload = json.dumps(data, ensure_ascii=False)
# Defensive: keep the payload safe inside a <script> block.
payload = payload.replace("</", "<\\/")

template = (ROOT / "index.template.html").read_text(encoding="utf-8")
if "__DATA__" not in template:
    sys.exit("Build failed: __DATA__ marker not found in template.")
out = template.replace("__DATA__", payload)
# newline="\n": deterministic LF output so the build is byte-reproducible
# across platforms (the committed seed uses LF; Windows would otherwise emit CRLF).
(ROOT / "index.html").write_text(out, encoding="utf-8", newline="\n")
print(f"Built index.html ({len(out):,} bytes), {len(candidates)} candidates embedded.")

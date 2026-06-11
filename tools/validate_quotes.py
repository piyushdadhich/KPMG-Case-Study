#!/usr/bin/env python3
"""Quote-grounding validator.

Checks that every evidence quote in every extraction JSON exists VERBATIM
(exact substring match) in its corresponding candidate submission, and that
the extraction conforms to the schema's hard rules (valid signal ids,
valid strength labels, all six signals present).

Exit code 0 = all checks pass. Non-zero = at least one failure.
This is a deterministic control: AI generates, this script verifies.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "candidates"
EXTRACTIONS = ROOT / "data" / "extractions"
VALID_SIGNALS = ["S1", "S2", "S3", "S4", "S5", "S6"]
VALID_STRENGTH = {"demonstrated", "described", "asserted"}

failures = []
total_quotes = 0

for ext_path in sorted(EXTRACTIONS.glob("*.json")):
    sub_id = ext_path.stem
    src_path = CANDIDATES / f"{sub_id}.md"
    if not src_path.exists():
        failures.append(f"{sub_id}: no matching candidate file {src_path.name}")
        continue
    source = src_path.read_text(encoding="utf-8")
    data = json.loads(ext_path.read_text(encoding="utf-8"))

    if data.get("submission_id") != sub_id:
        failures.append(f"{sub_id}: submission_id mismatch ({data.get('submission_id')})")

    signal_ids = [s.get("signal_id") for s in data.get("signals", [])]
    if signal_ids != VALID_SIGNALS:
        failures.append(f"{sub_id}: signals must be exactly S1..S6 in order, got {signal_ids}")

    for sig in data.get("signals", []):
        for ev in sig.get("evidence", []):
            total_quotes += 1
            quote = ev.get("quote", "")
            if not quote:
                failures.append(f"{sub_id}/{sig.get('signal_id')}: empty quote")
            elif quote not in source:
                failures.append(
                    f"{sub_id}/{sig.get('signal_id')}: NOT GROUNDED -> {quote[:70]!r}"
                )
            if ev.get("strength") not in VALID_STRENGTH:
                failures.append(
                    f"{sub_id}/{sig.get('signal_id')}: invalid strength {ev.get('strength')!r}"
                )
        if not sig.get("evidence") and not sig.get("interview_probes"):
            failures.append(
                f"{sub_id}/{sig.get('signal_id')}: empty signal must carry an interview probe"
            )

print(f"Checked {total_quotes} quotes across {len(list(EXTRACTIONS.glob('*.json')))} extractions.")
if failures:
    print(f"FAIL — {len(failures)} problem(s):")
    for f in failures:
        print("  ✗", f)
    sys.exit(1)
print("PASS — every quote is grounded verbatim; schema rules hold.")

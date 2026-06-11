# CLAUDE.md — Evidence Workbench conventions

## Design system: LOCKED mode
Brand tokens are pinned; do NOT re-derive styles.
Tokens: Ledger Ink #1B2733 · Cool Paper #F4F6F8 · Audit Blue #1F4FBF ·
Highlighter #FFE873 · Verify Green #1F7A4D · Probe Amber #B45309.
Type: Fraunces (display) / IBM Plex Sans (body) / IBM Plex Mono (evidence).
Signature element: highlighter-marked verbatim quotes with live "grounded ✓"
stamps. Any UI change must preserve it.
Every UI task: define deliberate states for zero, missing, loading, and
no-match — never ship an accidental placeholder.

## Process-skill bindings (mandatory)
- New feature → brainstorming gate: spec approved BEFORE code.
- Any change touching data/extractions or the prompt → run
  tools/validate_quotes.py BEFORE and AFTER; both results in the report.
- tools/build.py is the only way to produce index.html (it gates on the
  validator). Never hand-edit index.html.
- Any completion claim → fresh verification evidence in the STOP report;
  a report with zero ⚠ flags deserves suspicion.
- Any bug → root cause before fix; 3 failed fixes → stop and question
  the architecture.

## Hard product rules (do not relax without a recorded decision)
1. The AI never scores, ranks, compares, or recommends candidates.
2. Evidence is verbatim-or-rejected (validator enforced).
3. A signal with no evidence yields an interview probe, never a penalty.
4. No demographic extraction or inference, anywhere.
5. Recording a decision requires a written rationale; all decisions are
   timestamped and exportable.

## Known-stale risk
If the JD changes, the rubric in tools/build.py and the traceability table
in README.md must be updated together — they are one artifact in two places.

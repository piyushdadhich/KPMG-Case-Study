"""Behavioral tests for tools/build.py — the validator-gated producer.

The build must refuse to run on invalid data, must fully substitute the
__DATA__ marker, and must emit a payload that (a) parses as JSON, (b) carries
the full rubric + three candidates, (c) keeps every quote grounded in its
embedded source, and (d) contains no literal "</" that could break the
surrounding <script> block.
"""
import json
import re

from conftest import load_json, save_json

ENG = "data/extractions/ENG-01.json"

PRE = "window.WORKBENCH_DATA = "
POST = ";\n(function(){"


def build_html(repo, run):
    r = run(repo, "build.py")
    assert r.returncode == 0, f"build failed: {r.stdout}\n{r.stderr}"
    return (repo / "index.html").read_text(encoding="utf-8")


def extract_payload(html):
    """Return the raw JSON text assigned to window.WORKBENCH_DATA."""
    start = html.index(PRE) + len(PRE)
    end = html.index(POST, start)
    return html[start:end]


def test_build_blocks_when_validation_fails(repo, run):
    data = load_json(repo / ENG)
    data["signals"][0]["evidence"][0]["quote"] = "fabricated span absent from the source"
    save_json(repo / ENG, data)
    r = run(repo, "build.py")
    assert r.returncode != 0
    assert "Build blocked" in r.stderr
    assert not (repo / "index.html").exists()  # nothing written on a blocked build


def test_build_replaces_data_marker(repo, run):
    html = build_html(repo, run)
    assert "__DATA__" not in html


def test_build_embedded_json_parses(repo, run):
    html = build_html(repo, run)
    payload = extract_payload(html)
    data = json.loads(payload)  # \/ escaping is valid JSON; loads must succeed
    assert isinstance(data, dict)
    assert "rubric" in data and "candidates" in data


def test_build_embeds_three_candidates_and_six_signals(repo, run):
    html = build_html(repo, run)
    data = json.loads(extract_payload(html))
    assert [r["id"] for r in data["rubric"]] == ["S1", "S2", "S3", "S4", "S5", "S6"]
    assert len(data["candidates"]) == 3
    for c in data["candidates"]:
        ids = [s["signal_id"] for s in c["extraction"]["signals"]]
        assert ids == ["S1", "S2", "S3", "S4", "S5", "S6"]


def test_built_quotes_ground_against_embedded_sources(repo, run):
    html = build_html(repo, run)
    data = json.loads(extract_payload(html))
    total = 0
    for c in data["candidates"]:
        for sig in c["extraction"]["signals"]:
            for ev in sig["evidence"]:
                total += 1
                assert ev["quote"] in c["source"], f"{c['id']}/{sig['signal_id']} ungrounded"
    assert total == 30


def test_no_script_breakout_in_payload(repo, run):
    html = build_html(repo, run)
    payload = extract_payload(html)
    # build.py replaces every "</" with "<\/" before embedding, so the payload
    # region must contain no literal "</" that could close the <script> early.
    assert "</" not in payload

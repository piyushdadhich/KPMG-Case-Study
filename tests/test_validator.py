"""Behavioral tests for tools/validate_quotes.py — the deterministic control.

Green path: the seed passes and counts exactly 30 quotes across 3 files.
Red paths: each schema/grounding rule, corrupted one at a time in a tmp copy,
must drive a non-zero exit and the matching per-failure line.
"""
from conftest import load_json, save_json

ENG = "data/extractions/ENG-01.json"


def test_validator_passes_on_seed_data(repo, run):
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 0, r.stderr
    assert "every quote is grounded verbatim; schema rules hold." in r.stdout


def test_validator_counts_thirty_quotes_on_seed(repo, run):
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 0, r.stderr
    assert "Checked 30 quotes across 3 extractions." in r.stdout


def test_fails_on_ungrounded_quote(repo, run):
    data = load_json(repo / ENG)
    data["signals"][0]["evidence"][0]["quote"] = "this span does not appear in the source at all"
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "NOT GROUNDED" in r.stdout


def test_fails_on_empty_quote(repo, run):
    data = load_json(repo / ENG)
    data["signals"][0]["evidence"][0]["quote"] = ""
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "empty quote" in r.stdout


def test_fails_on_invalid_strength_label(repo, run):
    data = load_json(repo / ENG)
    data["signals"][0]["evidence"][0]["strength"] = "strong"  # not in the allowed three
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "invalid strength" in r.stdout


def test_fails_on_wrong_signal_order(repo, run):
    data = load_json(repo / ENG)
    # swap S2 and S3 so the ordered ids become S1, S3, S2, S4, S5, S6
    data["signals"][1], data["signals"][2] = data["signals"][2], data["signals"][1]
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "signals must be exactly S1..S6 in order" in r.stdout


def test_fails_on_submission_id_mismatch(repo, run):
    data = load_json(repo / ENG)
    data["submission_id"] = "ZZZ-99"  # no longer matches the filename stem
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "submission_id mismatch" in r.stdout


def test_fails_on_missing_candidate_file(repo, run):
    (repo / "data/candidates/ENG-01.md").unlink()
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "no matching candidate file" in r.stdout


def test_fails_when_empty_signal_lacks_probe(repo, run):
    data = load_json(repo / ENG)
    s4 = data["signals"][3]
    assert s4["signal_id"] == "S4" and s4["evidence"] == []  # the seed's empty signal
    s4["interview_probes"] = []  # strip its only probe
    save_json(repo / ENG, data)
    r = run(repo, "validate_quotes.py")
    assert r.returncode == 1
    assert "empty signal must carry an interview probe" in r.stdout

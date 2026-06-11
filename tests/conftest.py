"""Shared fixtures for the Evidence Workbench test suite.

Tests NEVER touch the seed files. Every test that exercises the validator or
the build runs against a throwaway copy of the repo under pytest's tmp_path,
created by the `repo` fixture. The tools derive their ROOT from their own
location (Path(__file__).parent.parent), so copying tools/ + data/ + the
template into a temp dir is enough to retarget them — no tool edits needed.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SEED = Path(__file__).resolve().parent.parent


@pytest.fixture
def repo(tmp_path):
    """A writable copy of the seed (tools/, data/, index.template.html)."""
    shutil.copytree(SEED / "tools", tmp_path / "tools")
    shutil.copytree(SEED / "data", tmp_path / "data")
    shutil.copy(SEED / "index.template.html", tmp_path / "index.template.html")
    return tmp_path


@pytest.fixture
def run():
    """Run a tool script inside a copied repo and capture its result.

    PYTHONUTF8=1 forces the child's stdout to UTF-8 so the validator's
    non-ASCII output ('—', '✗') is captured deterministically regardless of
    the Windows console code page.
    """
    def _run(root, tool):
        env = {**os.environ, "PYTHONUTF8": "1"}
        return subprocess.run(
            [sys.executable, str(root / "tools" / tool)],
            capture_output=True, text=True, encoding="utf-8", env=env,
        )
    return _run


# --- small JSON helpers for corrupting a tmp extraction in-place ---

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")

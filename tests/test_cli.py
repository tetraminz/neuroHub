"""Invoke the CLI and check output."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_runs(tmp_path) -> None:
    """CLI should exit cleanly and print accuracy."""
    result = subprocess.run(
        [sys.executable, str(Path("scripts/run_pipeline.py")), "--out", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "accuracy" in result.stdout.lower()

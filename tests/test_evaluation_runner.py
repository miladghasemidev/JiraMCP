from __future__ import annotations

from tools.run_evaluations import run


def test_deterministic_release_evaluations_pass_all_hard_gates() -> None:
    report = run()
    assert report["summary"]["total"] == 170
    assert report["summary"]["passed"] == 170
    assert report["summary"]["failed"] == 0
    assert report["summary"]["hard_failures"] == 0
    assert report["summary"]["pass_rate"] == 1.0

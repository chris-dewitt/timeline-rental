"""Tests for SQLite save/load."""

from timeline_rental.data.db import latest_run, list_runs, save_run


def test_save_and_load_run(tmp_path, monkeypatch):
    monkeypatch.setenv("SAVES_DIR", str(tmp_path))

    run_id = save_run(
        {
            "tape": "blade runner [damaged]",
            "choice_history": [0, 1],
            "outcome_index": 1,
            "measured_bitstring": "110",
            "narration": "The street was empty.",
            "receipt_line": "collapsed: timeline B",
            "lost_timelines": ["A", "C"],
            "photo_label": "empty street",
        }
    )

    latest = latest_run()
    assert latest is not None
    assert latest["id"] == run_id
    assert latest["outcome_index"] == 1
    assert len(list_runs()) >= 1

"""Tests for quantum timeline collapse."""

from timeline_rental.quantum.collapse import collapse_timeline


def test_collapse_returns_valid_outcome():
    result = collapse_timeline([0, 1], seed=42)
    assert result.outcome_index in (0, 1, 2)
    assert len(result.measured_bitstring) == 3


def test_collapse_reproducible():
    a = collapse_timeline([1], seed=99)
    b = collapse_timeline([1], seed=99)
    assert a.outcome_index == b.outcome_index
    assert a.measured_bitstring == b.measured_bitstring

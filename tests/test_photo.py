"""Tests for quantum photo superposition."""

from timeline_rental.quantum.photo import glitch_variant, photo_superposition


def test_photo_superposition_three_variants():
    sup = photo_superposition(42)
    assert len(sup.weights) == 3
    assert abs(sum(sup.weights) - 1.0) < 0.01
    assert sup.dominant_variant in (0, 1, 2)


def test_photo_superposition_reproducible():
    a = photo_superposition(7)
    b = photo_superposition(7)
    assert a.weights == b.weights


def test_glitch_variant_cycles():
    weights = (0.2, 0.3, 0.5)
    variants = {glitch_variant(f, weights) for f in range(100)}
    assert len(variants) >= 2

"""Validation of core.py against the source cited in README.md (`validation:`).

Replace this placeholder with closed-form / textbook values and scaling checks.
"""

import pytest

from .core import example


def test_example():
    assert example(2.5) == pytest.approx(2.5)

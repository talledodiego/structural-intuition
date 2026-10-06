"""Every key exists in both languages."""

from shared.i18n import missing_keys

from .strings import STRINGS


def test_strings_consistent():
    assert missing_keys(STRINGS) == []

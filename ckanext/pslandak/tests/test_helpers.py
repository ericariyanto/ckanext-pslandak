"""Tests for helpers.py."""

import ckanext.pslandak.helpers as helpers


def test_pslandak_hello():
    assert helpers.pslandak_hello() == "Hello, pslandak!"

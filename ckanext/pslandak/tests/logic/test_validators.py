"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.pslandak.logic import validators


def test_pslandak_reauired_with_valid_value():
    assert validators.pslandak_required("value") == "value"


def test_pslandak_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.pslandak_required(None)

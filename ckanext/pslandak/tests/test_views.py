"""Tests for views.py."""

import pytest

import ckanext.pslandak.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "pslandak")
@pytest.mark.usefixtures("with_plugins")
def test_pslandak_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("pslandak.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, pslandak!"

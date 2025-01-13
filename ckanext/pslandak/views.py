from flask import Blueprint


pslandak = Blueprint(
    "pslandak", __name__)


def page():
    return "Hello, pslandak!"


pslandak.add_url_rule(
    "/pslandak/page", view_func=page)


def get_blueprints():
    return [pslandak]

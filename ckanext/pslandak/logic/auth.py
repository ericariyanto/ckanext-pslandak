import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def pslandak_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "pslandak_get_sum": pslandak_get_sum,
    }

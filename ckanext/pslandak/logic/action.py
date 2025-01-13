import ckan.plugins.toolkit as tk
import ckanext.pslandak.logic.schema as schema


@tk.side_effect_free
def pslandak_get_sum(context, data_dict):
    tk.check_access(
        "pslandak_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.pslandak_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'pslandak_get_sum': pslandak_get_sum,
    }

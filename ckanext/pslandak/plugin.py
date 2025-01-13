from typing import Any, cast
from ckan.types import Context, Schema, Validator, ValidatorFactory
import logging

from ckan.common import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json


import ckanext.pslandak.cli as cli
# import ckanext.pslandak.helpers as helpers
# import ckanext.pslandak.views as views
# from ckanext.pslandak.logic import (
#     action, auth, validators
# )

def group_list():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'title asc', 'all_fields': True, 'include_dataset_count': False})

    # Truncate the list to the 10 most popular groups only.
    # groups = groups[:10]

    return groups

def format_number(number):
    formatted = "{:,.0f}".format(number).replace(",", ".")
    return formatted

def get_visualization():
    return config.get('ckanext.pslandak.visualization', '')

def get_metadata_fields():
    metafields = config.get('ckanext.pslandak.metadata_fields', '')
    if not metafields:
        return []
    return json.loads(metafields)

def get_metadata_keys_fields():
    metafields = get_metadata_fields()
    return [item['key'] for item in metafields]

def get_metadata_object(extras, key):
    result = {}
    for item in extras:
        if item['key'] == key:
            result = item
            break  # Keluar dari loop setelah menemukan yang cocok
    return result

def get_metadata_object_val(extras, key):
    obj = get_metadata_object(extras, key)
    if ( 'value' in obj ) :
        return obj['value']
    return None

def prepare_metadata_form():
    custom_fields = {}
    metakeys = get_metadata_keys_fields()
    for key in metakeys :
        custom_fields[key] = [
            toolkit.get_converter('convert_from_extras'),
            toolkit.get_validator('ignore_missing')
        ]
    return custom_fields

def no_registering(context, data_dict):
    return {
        'success': False,
        'msg': toolkit._(
            'You cannot register for this site.'
        )
    }

class PslandakPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    # plugins.implements(plugins.IAuthFunctions)
    # plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IValidators)
    

    # IConfigurer

    def get_auth_functions(self):
        return {
            'user_create': no_registering
        }

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "pslandak")

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')

        schema.update({
            'ckanext.pslandak.visualization': [ignore_missing, unicode_safe],
            'ckanext.pslandak.metadata_fields': [ignore_missing, unicode_safe],
        })

        return schema

    # IAuthFunctions

    def get_commands(self):
        return cli.get_commands()

    # ITemplateHelpers

    def get_helpers(self):
        '''Register the group_list() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'pslandak_group_list': group_list, 
            'pslandak_format_number' : format_number, 
            'pslandak_get_visualization': get_visualization,
            'pslandak_get_metadata_fields': get_metadata_fields,
            'pslandak_get_metadata_keys_fields': get_metadata_keys_fields,
            'pslandak_get_metadata_object': get_metadata_object,
            'pslandak_get_metadata_object_val': get_metadata_object_val,
        }
    
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True
    
    def package_types(self) -> list[str]:
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    def _modify_package_schema(self, schema: Schema):
        # for _key in get_metadata_keys_fields() :
        #     schema.update({
        #         _key : [toolkit.get_validator('ignore_missing'),
        #             toolkit.get_converter('convert_to_extras')]
        #         })
        
        # # # Add our custom_resource_text metadata field to the schema
        # # cast(Schema, schema['resources']).update({
        # #         'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
        # #         })

        self.write_log('_modify_package_schema')
        self.write_log(schema['resources'])

        return schema
    
    def create_package_schema(self) -> Schema:
        self.write_log('create_package_schema')
        schema: Schema = super(PslandakPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self) -> Schema:
        self.write_log('update_package_schema')
        schema: Schema = super(PslandakPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self) -> Schema:
        self.write_log('show_package_schema updated')
        schema: Schema = super(PslandakPlugin, self).show_package_schema()        
        # schema = self._modify_package_schema(schema)
        self.write_log(schema)

        return schema
    
    def write_log(self, object):
        logger = logging.getLogger(__name__)
        logger.debug(object)

    # IValidators

    # def get_validators(self):
    #     return validators.get_validators()
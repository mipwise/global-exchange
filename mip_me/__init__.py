__version__ = "0.1.0"
from mip_me.schemas import input_schema, output_schema
from mip_me.action_preprocess_data import preprocess_data
from mip_me.main import solve


# actions_config = {
#     'Action Name': {
#         'schema': 'input',
#         'engine': action_solve,
#         'tooltip': "A hint for what the engine do"},
#     }

input_tables_config = {
    'hidden_tables': ['parameters'],
    'categories': {},
    'order': list(),
    'tables_display_names': {},
    'columns_display_names': {},
    'hidden_columns': {}
    }

output_tables_config = {
    'hidden_tables': list(),
    'categories': dict(),
    'order': [],
    'tables_display_names': dict(),
    'columns_display_names': dict(),
    'hidden_columns': dict()
    }

parameters_config = {
    'hidden': ['MIP Gap', 'Time Limit (s)'],
    'categories': {},
    'order': [],
    'tooltips': {}
    }

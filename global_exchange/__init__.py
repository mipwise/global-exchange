__version__ = "1.0.0"
from global_exchange.schemas import input_schema, output_schema
from global_exchange.main import solve


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
    'hidden_columns': dict(),
    }

parameters_config = {
    'hidden': ['MIP Gap', 'Time Limit (s)'],
    'categories': {},
    'order': [],
    'tooltips': {},
    }

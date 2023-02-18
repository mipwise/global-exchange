"""
Defines the input and output schemas of the problem.
For more details on how to implement and configure data schemas see:
https://github.com/mipwise/mip-go/tree/main/5_develop/4_data_schema
"""

from ticdat import PanDatFactory

# region Aliases for datatypes in ticdat
# Remark: use only aliases that match perfectly your needs, otherwise set datatype explicitly
float_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": -float("inf"),
    "inclusive_min": False,
}

non_negative_float = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": 0,  # min=0
    "inclusive_min": True,
}

integer_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": -float("inf"),
    "inclusive_min": False,
}

non_negative_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 0,
    "inclusive_min": True,
}

positive_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 1,
    "inclusive_min": True,
}

text = {
    "strings_allowed": "*",
    "number_allowed": False
}
# endregion


# region INPUT SCHEMA
input_schema = PanDatFactory(
    parameters=[['Name'], ['Value']],
    rates=[['From', 'To', 'Tier ID'], ['Exchange Rate', 'National Fee', 'Tier Start', 'Tier End', 'International Fee']],
    requirements=[['Symbol'], ['Currency', 'Surplus', 'Max Surplus', 'Requirements', 'Balance']],
)
# endregion

# region USER PARAMETERS
input_schema.add_parameter(name="Time Limit (s)", default_value=30, **non_negative_float)
input_schema.add_parameter(
    name="MIP Gap",
    default_value=0.001,
    number_allowed=True,
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=1,
    inclusive_max=False,
    strings_allowed=()
)
# input_schema.add_parameter(name="Exchange Fee", default_value=0.01, **non_negative_float)
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    trades=[['From', 'To'], ['Quantity']],
    final_position=[['Symbol'], ['Quantity']],
    kpis=[['KPI'], ['Value']]
)
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA
# region rates
table = 'rates'
input_schema.set_data_type(table=table, field='From', **text)
input_schema.set_data_type(table=table, field='To', **text)
input_schema.set_data_type(table=table, field='Tier ID', **positive_integer)
input_schema.set_data_type(table=table, field='Exchange Rate', **non_negative_float)
input_schema.set_data_type(table=table, field='National Fee', **non_negative_float)
input_schema.set_data_type(table=table, field='Tier Start', **non_negative_float)
input_schema.set_data_type(table=table, field='Tier End', **non_negative_float)
input_schema.set_data_type(table=table, field='International Fee', **non_negative_float)
# endregion

# region requirements
table = 'requirements'
input_schema.set_data_type(table=table, field='Symbol', **text)
input_schema.set_data_type(table=table, field='Currency', **text)
input_schema.set_data_type(table=table, field='Surplus', **non_negative_float)
input_schema.set_data_type(table=table, field='Max Surplus', **non_negative_float, nullable=True)
input_schema.set_data_type(table=table, field='Requirements', **non_negative_float)
input_schema.set_data_type(table=table, field='Balance', **float_number)
# endregion

# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA
# region trades
table = 'trades'
output_schema.set_data_type(table=table, field='From', **text)
output_schema.set_data_type(table=table, field='To', **text)
output_schema.set_data_type(table=table, field='Quantity', **non_negative_float)
# endregion

# region trades
table = 'final_position'
output_schema.set_data_type(table=table, field='Symbol', **text)
output_schema.set_data_type(table=table, field='Quantity', **non_negative_float)
# endregion

# region kpis
table = 'kpis'
output_schema.set_data_type(table=table, field='KPI', **text)
output_schema.set_data_type(table=table, field='Value', **float_number)
# endregion

# endregion
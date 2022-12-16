from ticdat import PanDatFactory

# INPUT TABLE
input_schema = PanDatFactory(
    parameters=[['Parameter'], ['Value']],
    indices=[['symbol'],[]],
    rates=[['from', 'to'], ['rates']],
    requirements=[['symbol'], ['currency', 'surplus', 'requirements']])

table='rates'
input_schema.set_data_type(
    table=table,
    field='from',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table=table,
    field='to',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table=table,
    field='rates',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)

# REQUIREMENTS TABLE
table='requirements'
input_schema.set_data_type(
    table=table,
    field='symbol',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table=table,
    field='currency',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table=table,
    field='surplus',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)

input_schema.set_data_type(
    table=table,
    field='requirements',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)

# OUTPUT TABLE
output_schema = PanDatFactory(
    trades=[['from', 'to'], ['buy', 'sell']]
)

# TRADES TABLE
table='trades'
output_schema.set_data_type(
    table=table,
    field='from',
    number_allowed=False,
    strings_allowed='*')

output_schema.set_data_type(
    table=table,
    field='to',
    number_allowed=False,
    strings_allowed='*')

output_schema.set_data_type(
    table=table,
    field='buy',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=True,
    max=float('inf'),
    inclusive_max=False)

output_schema.set_data_type(
    table=table,
    field='sell',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=True,
    max=float('inf'),
    inclusive_max=False)
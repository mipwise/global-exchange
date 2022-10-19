from ticdat import PanDatFactory

input_schema = PanDatFactory(
    parameters=[['Parameter'], ['Value']],
    indices=[['symbol']],
    rates=[['from', 'to'], ['rates']],
    requirements=[['symbol'], ['currency', 'surplus', 'requirements']])

input_schema.set_data_type(
    table='rates',
    field='from',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table='rates',
    field='to',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table='rates',
    field='rate',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)

input_schema.set_data_type(
    table='requirements',
    field='symbol',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table='requirements',
    field='currency',
    number_allowed=False,
    strings_allowed='*')

input_schema.set_data_type(
    table='requirements',
    field='surplus',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)

input_schema.set_data_type(
    table='requirements',
    field='requirements',
    number_allowed=True,
    strings_allowed=(),
    must_be_int=False,
    min=0,
    inclusive_min=False,
    max=float('inf'),
    inclusive_max=False)


output_schema = PanDatFactory(
    trades=[['from', 'to'], ['buy', 'sell']]
)

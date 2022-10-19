
from itertools import product
from pathlib import Path

# import numpy as np
import pandas as pd
import pulp

# path to data files
req_path = Path.cwd() / 'mip_me' / 'test_mip_me' / 'data'\
    / 'inputs' / 'requirements.csv'

rates_path = Path.cwd() / 'mip_me' / 'test_mip_me' / 'data'\
    / 'inputs' / 'rates.csv'

idxs_path = Path.cwd() / 'mip_me' / 'test_mip_me' / 'data'\
    / 'inputs' / 'idxs.csv'

# read the data
idxs_df = pd.read_csv(idxs_path, index_col='symbol')
reqs_df = pd.read_csv(req_path, index_col='symbol')
rates_df = pd.read_csv(rates_path, usecols=['from', 'to', 'rate'])

reqs_df['total'] = reqs_df['requirements'] - reqs_df['surplus']


def get_rate(c_from: str, c_to: str):
    rate = rates_df.loc[
            (rates_df['from'] == c_from) &
            (rates_df['to'] == c_to), 'rate'].iloc[0]
    return rate


# number of currencies
n = len(idxs_df)

# print(reqs_df.loc['EUR',['surplus','requirements']])
I = [*idxs_df.index]

keys = [(i, j) for (i, j) in [*product(I, repeat=2)] if i != j]


# define the model
mdl = pulp.LpProblem('GlobalEx', sense=pulp.LpMaximize)

# define the variable
# x_ij = currency i to be exhanged by j
x = pulp.LpVariable.dicts(
    'x_',
    indices=keys,
    cat='Continuous',
    lowBound=0
    # upBound=1000
    )

# CONSTRAINTS
# flow balance for each currency: incoming-leaving >= required - surplis
for curr in I:
    mdl.addConstraint(
        pulp.lpSum(
            x[other, curr]*get_rate(other, curr) - x[curr, other]
            for other in I if other != curr) == reqs_df.loc[curr, 'total'],
        name=f'flow_{curr}'
        )

total_usd = pulp.lpSum(
    x[other, 'USD']*get_rate(other, 'USD') - x['USD', other]
    for other in (set(I)-{'USD'})
    )

mdl.setObjective(total_usd)

status = mdl.solve()

print(f'{pulp.LpSolution[status]}')

if status == 1:
    x_sol = {key: x[key].value() for key in keys if x[key].value() >= 0.0001}
    print(x_sol)

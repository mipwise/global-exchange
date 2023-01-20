
from itertools import product
from pathlib import Path

# import numpy as np
import pandas as pd
import pulp

from mip_me.schemas import input_schema, output_schema


# read the data
def get_rate(rates, c_from: str, c_to: str):
    rate = rates.loc[
            (rates['From'] == c_from) &
            (rates['To'] == c_to), 'Rate'].iloc[0]
    return rate


def fee(rates, c_from: str, c_to: str):
    fee = rates.loc[(rates['From'] == c_from) &
                     (rates['To'] == c_to), 'Total Fee'].iloc[0] 
    return fee


def get_optimization_data(dat):
    # params = dat.parameters.copy()
    idxs = dat.requirements['Symbol'].unique()
    # n = len(idxs)  # numbeer of currencies
    I = [*idxs]
    keys = [(i, j) for (i, j) in [*product(I, repeat=2)] if i != j]

    return keys, I


def solve(dat):
    keys, I = get_optimization_data(dat)
    mdl = pulp.LpProblem('GlobalEx', sense=pulp.LpMinimize)
    params = input_schema.create_full_parameters_dict(dat)
    # define the variable
    # x_ij = currency i to be exhanged by j
    x = pulp.LpVariable.dicts(
        'x_',
        indices=keys,
        cat='Continuous',
        lowBound=0,
        upBound=500,
        )

    # CONSTRAINTS
    # flow balance for each currency: incoming-leaving >= required - surplus
    for curr in (set(I) - {'USD'}):
        mdl.addConstraint(
            pulp.lpSum(
                x[other, curr] * get_rate(dat.rates, other, curr) * (1 - fee(dat.rates, other, curr)) - x[curr, other] 
                for other in I if other != curr) == dat.requirements.loc[dat.requirements['Symbol'] == curr]['Balance'].iloc[0],
            name=f'flow_{curr}'
            )

    # Dollar constraint (if you let it be >= you can explore the market!)
    mdl.addConstraint(
        pulp.lpSum(
            x[other, 'USD'] * get_rate(dat.rates, other, 'USD') * (1 - fee(dat.rates, other, 'USD')) - x['USD', other]
            for other in I if other != 'USD') >= dat.requirements.loc[dat.requirements['Symbol'] == 'USD']['Balance'].iloc[0],
        name='flow_USD'
        )

    # we are not allowed to buy another currencies with dollars (to prevent more cycles)
    # mdl.addConstraint(
    #     pulp.lpSum(x['USD', other] for other in I if other != 'USD') == 0, name='zero_outflow_USD'
    #     )

    # total_usd = pulp.lpSum(
    #     x[other, 'USD']*get_rate(dat.rates, other, 'USD') - x['USD', other]
    #     for other in (set(I) - {'USD'})
    #     )

    total_fees = pulp.lpSum(x[i, j] * (fee(dat.rates, i, j) * get_rate(dat.rates, i, 'USD')) for i,j in keys)

    mdl.setObjective(total_fees)

    mdl.solve(pulp.PULP_CBC_CMD(timeLimit=params['Time Limit (s)'], gapRel=params['MIP Gap']))
    status = pulp.LpStatus[mdl.status]
    sln = output_schema.PanDat()
    if status == 'Optimal':
        x_sol = [(*key, var.value()) for key, var in x.items() if var.value() >= 0.0001]
        sln.trades = pd.DataFrame(x_sol, columns=['From', 'To', 'Quantity'])
        sln.kpis = pd.DataFrame({'KPI': ['Total Fee ($k)'], 'Value': [mdl.objective.value() * 1000]})
        sln.final_position = pd.DataFrame(columns=['Symbol', 'Quantity'])
        for symb in I:
            new_row = pd.DataFrame({'Symbol': [symb], 'Quantity': [pulp.lpSum(x[other, symb].value() * get_rate(dat.rates, other, symb) - x[symb, other].value()
                                                                   for other in (set(I) - {symb}))]})
            sln.final_position = pd.concat([sln.final_position, new_row], ignore_index=True)
    
    else:
        print(f'Model is not optimal. Status: {status}')

    return sln

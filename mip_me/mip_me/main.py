
from itertools import product
from pathlib import Path

# import numpy as np
import pandas as pd
import pulp
from pulp import lpSum

from mip_me.schemas import input_schema, output_schema


# read the data
def get_rate(rates, c_from: str, c_to: str):
    rate = rates.loc[
            (rates['From'] == c_from) &
            (rates['To'] == c_to), 'Exchange Rate'].iloc[0]
    return rate


def fee(rates, c_from: str, c_to: str):
    fee = rates.loc[(rates['From'] == c_from) &
                     (rates['To'] == c_to), 'Total Fee'].iloc[0] 
    return fee


def get_optimization_data(dat):
    # params = input_schema.create_full_parameters_dict(dat)
    idxs = dat.requirements['Symbol'].unique()
    I = [*idxs]
    K = dict()
    for (i, j), group_df in dat.rates[['From', 'To', 'Tier ID']].groupby(['From', 'To']):
        list_of_tiers_ids = sorted(list(set(group_df['Tier ID'])))
        # assert 0 is not a Tier ID
        assert 0 not in list_of_tiers_ids, \
            f"The list of 'Tier ID' in the trade of currency {i} by currency {j} cannot contain 0"
        # the list of breakpoints includes the 0
        K[i, j] = [0] + list_of_tiers_ids
    du = dict(zip(dat.requirements['Symbol'], dat.requirements['Max Surplus']))
    b = dict(zip(dat.requirements['Symbol'], dat.requirements['Surplus']))
    dl = dict(zip(dat.requirements['Symbol'], dat.requirements['Requirements']))
    # the x and y keys are the pairs to be traded
    x_keys = [(i, j) for (i, j) in [*product(I, repeat=2)] if i != j]
    y_keys = x_keys.copy()
    # z_keys are triples (i, j, k) where k are the tiers of the variable fee (1, 2, ...) [don't include 0]
    z_keys = [(i, j, k) for i, j in x_keys for k in K[i, j] if k != 0]
    # w_keys are triples (i, j, k) where k are the breakpoints of the tiers [include 0]
    w_keys = [(i, j, k) for i, j in x_keys for k in K[i, j]]
    # bx: are the x value of the brakpoints (amount to be traded), of the form {('From', 'To', "Tier ID"): bx}
    bx = dict(zip(zip(dat.rates['From'], dat.rates['To'], dat.rates['Tier ID']), dat.rates['Tier End']))
    bx.update({(i, j, 0): 0 for i, j in x_keys})

    # create a dictionary: {'From', 'To', 'Tier ID'): by_accumulated_fee}
    fee_tiers_df = dat.rates.copy()
    fee_tiers_df['Difference Tier End'] = fee_tiers_df['Tier End'] - fee_tiers_df['Tier Start']
    fee_tiers_df['Fee in Each Tier'] = fee_tiers_df['International Fee'] * fee_tiers_df['Difference Tier End']
    fee_tiers_df['Cumulative Fee'] = fee_tiers_df.groupby(['From', 'To'])['Fee in Each Tier'].cumsum()
    by = dict(zip(
        zip(fee_tiers_df['From'], fee_tiers_df['To'], fee_tiers_df['Tier ID']),
        fee_tiers_df['Cumulative Fee']
    ))
    by.update({(i, j, 0): 0 for i, j in y_keys})
    # create dictionary of the fixed fees: {('From', 'To'): fee}
    f = dict(zip(zip(dat.rates['From'], dat.rates['To']),
                 dat.rates['National Fee']))
    # create dictionary of exchange rates
    r = dict(zip(zip(dat.rates['From'], dat.rates['To']),
                 dat.rates['Exchange Rate']))

    return I, K, bx, by, b, dl, du, f, r, x_keys, y_keys, z_keys, w_keys


def solve(dat):
    I, K, bx, by, b, dl, du, f, r, x_keys, y_keys, z_keys, w_keys = get_optimization_data(dat)
    mdl = pulp.LpProblem('GlobalEx', sense=pulp.LpMinimize)
    params = input_schema.create_full_parameters_dict(dat)
    # define the variable
    # x_ij = currency i to be exhanged by j
    x = pulp.LpVariable.dicts('x_', indices=x_keys, cat='Continuous', lowBound=0)
    # Total fee cost when exchanging i per j
    y = pulp.LpVariable.dicts('y_', indices=x_keys, cat='Continuous', lowBound=0)
    # Weight of the breakpoint k when exchanging i per j
    w = pulp.LpVariable.dicts('w_', indices=w_keys, cat='Continuous', lowBound=0)
    # in what tier the operation falls in
    z = pulp.LpVariable.dicts('z_', indices=z_keys, cat='Binary')

    # ADD CONSTRAINTS
    # C1) Amount of currency as a weighted combination of the breakpoints
    for i, j in x_keys:
        mdl.addConstraint(x[i, j] == lpSum(bx[i, j, k] * w[i, j, k] for k in K[i, j]), name=f'C1_{i}_{j}')

    # C2) Total fee paid for exchanging currency i per currency j
    for i, j in y_keys:
        mdl.addConstraint(y[i, j] == x[i, j] * f[i, j] + lpSum(by[i, j, k] * w[i, j, k] for k in K[i, j]), name=f'C2_{i}_{j}')

    # C3) Flow of traded currencies must satisfy the demands of currency i
    for i in I:
        mdl.addConstraint(
            lpSum((x[j, i] - y[j, i]) * r[j, i] for j in (set(I) - {i})) - lpSum(x[i, j] for j in (set(I) - {i})) + b[i] >= dl[i],
            name=f'C3_{i}'
        )

    # C4) Final position of each currency must be below the Max Surplus
    # for i in (set(I) - {'USD'}):
    for i in I:
        mdl.addConstraint(
            lpSum((x[j, i] - y[j, i]) * r[j, i] for j in (set(I) - {i})) - lpSum(x[i, j] for j in (set(I) - {i})) + b[i] <= du[i],
            name=f'C4_{i}'
        )
    
    # C5) Weights add up to 1
    for i, j in x_keys:
        mdl.addConstraint(lpSum(w[i, j, k] for k in K[i, j]) == 1, name=f'C5_{i}_{j}')

    # C6) The weights associated with the extremes of tier k are non-zero only if the amount of currency i falls into tier k
    for i, j in x_keys:
        mdl.addConstraint(w[i, j, K[i, j][0]] <= z[i, j, K[i, j][1]], name=f'C6_{i}_{j}_{K[i,j][0]}')
        mdl.addConstraint(w[i, j, K[i, j][-1]] <= z[i, j, K[i, j][-1]], name=f'C6_{i}_{j}_{K[i,j][-1]}')
        for index, k in enumerate(K[i, j][1:-1]):
            mdl.addConstraint(w[i, j, k] <= z[i, j, k] + z[i, j, K[i, j][1:][index + 1]], name=f'C6_{i}_{j}_{k}')

    total_fees = lpSum(y[i, j] * r[i, 'USD'] for i, j in y_keys if i != 'USD')

    mdl.setObjective(total_fees)

    mdl.solve(pulp.PULP_CBC_CMD(timeLimit=params['Time Limit (s)'], gapRel=params['MIP Gap']))
    status = pulp.LpStatus[mdl.status]
    sln = output_schema.PanDat()
    if status == 'Optimal':
        x_sol = [(*key, x_var.value()) for key, x_var in x.items() if x_var.value() >= 0.0001]
        sln.trades = pd.DataFrame(x_sol, columns=['From', 'To', 'Quantity'])
        sln.kpis = pd.DataFrame({'KPI': ['Total Fee ($k)'], 'Value': [mdl.objective.value() * 1000]})
        sln.final_position = pd.DataFrame(columns=['Symbol', 'Quantity'])
        for symb in I:
            new_row = pd.DataFrame({'Symbol': [symb], 'Quantity': [lpSum((x[other, symb].value() - y[other, symb].value()) * r[other, symb] - x[symb, other].value()
                                                                   for other in (set(I) - {symb})) + b[symb]]})
            sln.final_position = pd.concat([sln.final_position, new_row], ignore_index=True)
    
    else:
        print(f'Model is not optimal. Status: {status}')

    return sln

import pandas as pd
from pathlib import Path
from mip_me.schemas import input_schema


def preprocess_data(conv_path: Path, reqs_path: Path) -> input_schema.PanDat:
    """Read csv files from conv_path and reqs_path and populate the input schema.

    Parameters
    ----------
    conv_path : str
        path to csv file containing the conversion tables.
    reqs_path : str
        path to csv file containing the requirements and surpluses.

    Returns
    -------
    PanDat()
        return a PanDat object.
    """

    requirements_df = pd.read_csv(reqs_path).sort_values('symbol').rename(columns={'currency': 'Currency', 'symbol': 'Symbol', 'surplus': 'Surplus', 'requirements': 'Requirements'})
    conversion_df = pd.read_csv(conv_path, index_col=['currency']).T.reset_index(names=['symbol'])
    rate_df = pd.melt(conversion_df, id_vars=['symbol']).sort_values(['symbol', 'currency'], ignore_index=True).rename(columns={'symbol': 'From', 'currency': 'To', 'value': 'Rate'})
    rate_df.astype({'From': 'object', 'To': 'object', 'Rate': 'float'})
    requirements_df['Balance'] = requirements_df['Requirements'] - requirements_df['Surplus']

    dat = input_schema.PanDat()
    # dat.parameters = pd.DataFrame({'Name': ['MIP Gap', 'Time Limit (s)'], 'Value': [0.001, 30]})
    dat.rates = rate_df[['From', 'To', 'Rate']].copy()
    dat.requirements = requirements_df[['Symbol', 'Currency', 'Surplus', 'Requirements', 'Balance']].copy()

    return dat


 






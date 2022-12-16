import pandas as pd

from mip_me import input_schema


def data_preprocessing(conv_path: str(), reqs_path: str()):
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

    # read conversion table
    conv_df = pd.read_csv(conv_path, index_col='currency')
    conv_df = conv_df.T.reset_index(names=['symbol'])

    # create a dataframe with the conversion rates
    rate_df = pd.melt(conv_df, id_vars=['symbol'])
    rate_df.columns = ['from', 'to', 'rate']
    
    reqs_df = pd.read_csv(reqs_path, index_col='symbol')

    # create index dataframe
    idx_df = pd.DataFrame(set(reqs_df.index), columns=['symbol'])

    dat = input_schema.PanDat()
    dat.indices = idx_df['symbol']
    dat.rates = rate_df[['from','to','rate']]
    dat.requirements = reqs_df[['symbol', 'currency', 'surplus', 'requirements']]

    return dat


 






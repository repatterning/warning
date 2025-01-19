import os

import dask.dataframe
import pandas as pd
import statsmodels.graphics.tsaplots as sgt


class Correlation:

    def __init__(self):
        pass

    def exc(self, listings: list):

        for listing in listings[:2]:

            data: pd.DataFrame = dask.dataframe.read_csv(os.path.join(listing, '*.csv')).compute()
            data.sort_values(by='timestamp', ascending=True, inplace=True)

            sgt.plot_pacf(x=data['value'].values)

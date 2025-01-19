import os
import matplotlib.pyplot as plt

import dask.dataframe
import pandas as pd
import statsmodels.graphics.tsaplots as sgt


class Correlation:

    def __init__(self):
        pass

    @staticmethod
    def exc(listings: list):
        """

        :param listings:
        :return:
        """

        for listing in listings[:2]:

            try:
                data: pd.DataFrame = dask.dataframe.read_csv(os.path.join(listing, '*.csv')).compute()
            except ImportError as err:
                raise err from err

            data.sort_values(by='timestamp', ascending=True, inplace=True)

            fig, ax = plt.subplots(1, 1, figsize=(4.1, 2.3))

            sgt.plot_pacf(x=data['value'].values, ax=ax)

            plt.show()



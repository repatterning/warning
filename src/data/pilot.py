import logging
import pandas as pd


class Pilot:

    def __init__(self, assets: pd.DataFrame):
        """

        :param assets:
        """

        self.__assets = assets

    def exc(self):
        """

        :return:
        """

        # Temporary
        catchments: pd.DataFrame = self.__assets[['catchment_id', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_name']).value_counts()

        catchments.reset_index(drop=False, inplace=True)

        logging.info('CATCHMENTS:\n%s', catchments)

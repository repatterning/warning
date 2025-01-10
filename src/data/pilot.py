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

        catchments: pd.Series = self.__assets[['catchment_id', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_name']).value_counts()

        latest = catchments.to_frame().reset_index()

        latest = latest.copy().sort_values(by='count', ascending=True)

        logging.info(latest)

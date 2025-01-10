"""Module pilot.py"""
import logging
import pandas as pd


class Pilot:
    """

    """

    def __init__(self, assets: pd.DataFrame):
        """

        :param assets:
        """

        self.__assets = assets

    def __catchments(self):

        numbers: pd.Series = self.__assets[['catchment_id', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_name']).value_counts()

        catchments = numbers.to_frame().reset_index()

        return catchments.copy().sort_values(by='count', ascending=True)

    def __slice(self):
        pass



    def exc(self):
        """

        :return:
        """

        catchments = self.__catchments()
        logging.info(catchments)

        conditionals = (catchments['count'] >= 5) & (catchments['count'] <=7)
        catchments = catchments.copy().loc[conditionals, :]
        logging.info(catchments)

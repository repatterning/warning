"""Module pilot.py"""
import pandas as pd

import config


class Pilot:
    """
    Extracts the initial set of stations/time-series codes.
    """

    def __init__(self, assets: pd.DataFrame):
        """

        :param assets:
        """

        self.__assets = assets

        # Configurations
        self.__configurations = config.Config()

    def __catchments(self):
        """
        The catchments with station counts within a minimum & maximum count limit.

        :return:
        """

        numbers: pd.Series = self.__assets[['catchment_id', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_name']).value_counts()

        catchments = numbers.to_frame().reset_index()

        return catchments.copy().sort_values(by='count', ascending=True)

    def __filter(self, catchments: pd.DataFrame) -> pd.DataFrame:
        """
        The assets of the stations within the selected catchment areas.

        :param catchments:
        :return:
        """

        # The <conditionals> variable is of type pandas.Series
        conditionals = ((catchments['count'] >= self.__configurations.minimum) &
                        (catchments['count'] <= self.__configurations.maximum))

        catchments: pd.Series = catchments.copy().loc[conditionals, 'catchment_id']

        return self.__assets.loc[self.__assets['catchment_id'].isin(catchments), :]

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        catchments = self.__catchments()
        assets = self.__filter(catchments=catchments)
        assets.info()

        return assets

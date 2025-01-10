"""Module interface.py"""
import logging
import pandas as pd

import config
import src.data.codes
import src.data.points
import src.data.rating
import src.data.stations
import src.data.assets
import src.functions.streams
import src.data.pilot


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    @staticmethod
    def __persist(blob: pd.DataFrame, path: str) -> str:
        """

        :param blob:
        :param path:
        :return:
        """

        streams = src.functions.streams.Streams()

        return streams.write(blob=blob, path=path)

    def __span(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        conditionals = (assets['from'] <= self.__configurations.starting) & (assets['to'] >= self.__configurations.at_least)
        assets = assets.loc[conditionals, :]
        assets.info()

        return assets

    def exc(self):
        """

        :return:
        """

        # Retrieving the codes of <level> sequences.
        codes = src.data.codes.Codes().exc()

        # Stations
        stations = src.data.stations.Stations().exc()

        # Assets; limit by requisite, i.e., available time span.
        assets = src.data.assets.Assets(codes=codes, stations=stations).exc()
        assets = self.__span(assets=assets.copy())

        # Pilot
        pilot = src.data.pilot.Pilot(assets=assets.copy()).exc()
        logging.info(pilot)

        # Rating
        src.data.rating.Rating().exc()

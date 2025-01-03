"""Module interface.py"""

import pandas as pd

import config
import src.functions.streams
import src.data.stations
import src.data.points


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations
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

    @staticmethod
    def exc():
        """

        :return:
        """

        src.data.stations.Stations().exc()
        src.data.points.Points().exc()

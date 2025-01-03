"""Module interface.py"""

import pandas as pd

import src.data.codes
import src.data.points
import src.data.rating
import src.data.stations
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

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

        # This class will retrieve the codes of the sequences in focus
        src.data.codes.Codes().exc()

        # Exploring stations
        src.data.stations.Stations().exc()

        # Rating
        src.data.rating.Rating().exc()

        # Upcoming; 56178010
        src.data.points.Points().exc(ts_id=56178010, period='P1M', datestr='2025-01-01')

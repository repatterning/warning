"""Module interface.py"""
import logging
import pandas as pd

import src.data.codes
import src.data.points
import src.data.rating
import src.data.stations
import src.data.assets
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

        # Retrieving the codes of <level> sequences.
        codes = src.data.codes.Codes().exc()

        # Stations
        stations = src.data.stations.Stations().exc()

        # <level> asset instances that (a) have a catchment size value, (b) have a gauge datum value,
        # (c) have a measuring station <on_river> indicator, (d) have <from> & <to>
        # date values of type datetime (%Y-%m-%d), (e) have longitude & latitude values
        # of type float, (f) have a water level time series identification code value, (g) and
        # more.  The <from> & <to> values encode the time span of a series.
        assets = src.data.assets.Assets(codes=codes, stations=stations)
        logging.info(assets)


        # Rating
        src.data.rating.Rating().exc()

        # Upcoming; 56178010, P1M => period 1 month, datestr will be the latest data
        src.data.points.Points().exc(ts_id=56178010, period='P1M', datestr='2025-01-01')

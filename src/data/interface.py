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

        # Assets
        assets = src.data.assets.Assets(codes=codes, stations=stations).exc()
        logging.info(assets.head())

        catchments: pd.DataFrame = assets[['catchment_id', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_name']).value_counts()
        logging.info('CATCHMENTS:\n%s', catchments)

        # Rating
        src.data.rating.Rating().exc()

        # Upcoming; 56178010, P1M => period 1 month, datestr will be the latest data
        src.data.points.Points().exc(ts_id=56178010, period='P1M', datestr='2025-01-01')

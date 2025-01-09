"""Module interface.py"""
import logging
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

        # Retrieving the codes of <level> sequences.
        codes = src.data.codes.Codes().exc()
        logging.info('codes: %s', codes.shape)

        # Stations
        stations = src.data.stations.Stations().exc()
        logging.info('stations: %s', stations.shape)


        left = ['station_id', 'catchment_id', 'stationparameter_no', 'parametertype_id', 'ts_id', 'ts_name', 'from', 'to']
        right = ['station_id', 'station_latitude', 'station_longitude', 'river_id',
                 'CATCHMENT_SIZE', 'GAUGE_DATUM', 'GROUND_DATUM']

        # Rating
        src.data.rating.Rating().exc()

        # Upcoming; 56178010, P1M => period 1 month, datestr will be the latest data
        src.data.points.Points().exc(ts_id=56178010, period='P1M', datestr='2025-01-01')

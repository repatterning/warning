"""Module interface.py"""
import datetime
import logging
import time

import pandas as pd

import src.algorithms.algorithm
import src.algorithms.points


class Interface:
    """
    The model building steps vis-à-vis a Bayesian Vector Autoregressive Algorithm
    """

    def __init__(self):
        """
        Constructor
        """

        self.__columns = ['value', 'catchment_size', 'gauge_datum', 'on_river']

        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """

        :return:
        """

        points: pd.DataFrame = src.algorithms.points.Points().exc()
        points.info()

        cutoff = datetime.datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        limit = 1000 * time.mktime(cutoff.timetuple())
        frame: pd.DataFrame = points.copy().loc[points['timestamp'] < limit, :]
        frame.sort_values(by=['station_id', 'timestamp'], ascending=True, inplace=True)

        src.algorithms.algorithm.Algorithm().exc(n_lags=2, frame=points, columns=self.__columns, groupings='station_id', _priors=False)

"""Module interface.py"""
import logging

import src.algorithms.points
import src.algorithms.algorithm


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

        points = src.algorithms.points.Points().exc()
        self.__logger.info(points.head())

        src.algorithms.algorithm.Algorithm().exc(n_lags=2, frame=points, columns=self.__columns, groupings='station_id', _priors=False)

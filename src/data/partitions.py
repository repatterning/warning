import logging
import pandas as pd
import numpy as np
import datetime

import config

import src.elements.partitions as prt


class Partitions:

    def __init__(self, pilot: pd.DataFrame):
        """
        'station_id', 'catchment_id', 'catchment_name', 'ts_id', 'ts_name', 'from', 'to',
        'stationparameter_no', 'parametertype_id', 'station_latitude', 'station_longitude', 'river_id',
        'CATCHMENT_SIZE', 'GAUGE_DATUM'

        :param pilot:
        """

        self.__pilot = pilot

        # Configurations
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __matrix(self, datestr: np.datetime64):

        data = self.__pilot.copy()
        data = data.assign(period = datestr)

        self.__logger.info(data.to_dict(orient='index'))


    def exc(self):

        dates = pd.date_range(
            start=self.__configurations.starting, end=self.__configurations.at_least, freq='MS').to_frame(
            index=False, name='date')
        values: pd.Series = dates['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        self.__logger.info(type(values))

        for datestr in values.values:

            self.__logger.info(type(datestr))
            self.__logger.info(str(datestr))

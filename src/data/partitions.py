import logging
import pandas as pd
import numpy as np
import datetime

import config

import src.elements.partitions as prt


class Partitions:

    def __init__(self, data: pd.DataFrame):
        """
        'station_id', 'catchment_id', 'catchment_name', 'ts_id', 'ts_name', 'from', 'to',
        'stationparameter_no', 'parametertype_id', 'station_latitude', 'station_longitude', 'river_id',
        'CATCHMENT_SIZE', 'GAUGE_DATUM'

        :param data:
        """

        self.__data = data

        # Fields
        self.__fields = ['ts_id', 'period', 'catchment_size', 'gauge_datum', 'on_river']

        # Configurations
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __matrix(self, period: str):
        """

        :param period:
        :return:
        """

        data = self.__data.copy()
        data = data.assign(period = str(period))
        dictionary = data[self.__fields].to_dict(orient='index')

        logging.info(prt.Partitions(**dictionary))

    def exc(self):
        """

        :return:
        """

        frame = pd.date_range(start=self.__configurations.starting, end=self.__configurations.at_least, freq='MS'
                              ).to_frame(index=False, name='date')
        periods: pd.Series = frame['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        for period in periods.values:

            self.__matrix(period=period)

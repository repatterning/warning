import logging
import pandas as pd

import config


class Partitions:

    def __init__(self):

        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):

        dates = pd.date_range(start=self.__configurations.starting, end=self.__configurations.at_least, freq='MS')

        self.__logger.info(dates)

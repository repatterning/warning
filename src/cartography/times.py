"""Module cartography/times.py"""
import logging
import os

import geopandas

import config
import src.functions.objects


class Times:
    """
    The start & end times vis-à-vis a weather warning period.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def exc(self, data: geopandas.GeoDataFrame):
        """

        :param data:
        :return:
        """

        # The data
        data.info()
        self.__logger.info(data)
        self.__logger.info(data['ending'].max().strftime('%Y-%m-%d %H:%M:%S'))
        self.__logger.info(data['starting'].min().strftime('%Y-%m-%d %H:%M:%S'))

        # The time limits, and storage object
        nodes = {
            'starting': data['starting'].min().strftime('%Y-%m-%d %H:%M:%S'),
            'ending': data['ending'].max().strftime('%Y-%m-%d %H:%M:%S')
        }
        path = os.path.join(self.__configurations.warning_, 'times.json')

        # Persist
        objects = src.functions.objects.Objects()
        objects.write(nodes=nodes, path=path)

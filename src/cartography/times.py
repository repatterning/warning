import os
import logging

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

        data.info()
        self.__logger.info(data)
        self.__logger.info(data['ending'].max())
        self.__logger.info(data['starting'].min())

        nodes = {
            'starting': data['starting'].min(),
            'ending': data['ending'].max()
        }

        path = os.path.join(self.__configurations.warning_, 'times.json')

        objects = src.functions.objects.Objects()
        objects.write(nodes=nodes, path=path)

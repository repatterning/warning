
import logging

import geopandas


class Times:

    def __init__(self):


        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def exc(self, data: geopandas.GeoDataFrame):

        data.info()
        self.__logger.info(data)
        self.__logger.info(data['ending'].max())
        self.__logger.info(data['starting'].min())

        dictionary = {
            'starting': data['starting'].min(),
            'ending': data['ending'].max()
        }

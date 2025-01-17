
import logging

import src.algorithms.points


class Interface:

    def __init__(self):

        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def exc(self):

        points = src.algorithms.points.Points().exc()
        points.info()
        self.__logger.info(points.head())


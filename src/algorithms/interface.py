
import logging

import src.algorithms.points


class Interface:

    def __init__(self):
        pass

    def exc(self):

        points = src.algorithms.points.Points().exc()
        logging.info(points.head())
        points.info()

"""Module interface.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations
        self.__configurations = config.Config()

    @staticmethod
    def __persist(blob: pd.DataFrame, path: str) -> str:
        """

        :param blob:
        :param path:
        :return:
        """

        streams = src.functions.streams.Streams()

        return streams.write(blob=blob, path=path)

    @staticmethod
    def __data() -> pd.DataFrame:
        """

        :return:
        """

        abscissae = np.linspace(start=0, stop=1, num=101)
        ordinates = np.power(2, abscissae)

        return pd.DataFrame(
            data={'abscissa': abscissae, 'ordinate': ordinates})

    def exc(self, architecture: str):
        """

        :param architecture: The name of a machine learning architecture
        :return:
        """

        data = self.__data()
        logging.info(data)

        path = os.path.join(self.__configurations.storage, f'{architecture}.csv')
        message = self.__persist(blob=data, path=path)
        logging.info(message)

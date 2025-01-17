"""Module points.py"""
import glob
import logging
import os

import dask.dataframe
import pandas as pd

import config


class Points:
    """
    This class reads-in time series points
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()


    def __get_listings(self) -> list:
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.series_, '**', '*.csv'), recursive=True)

        return listings

    def __get_sections_codes(self) -> list:
        """

        :return:
        """

        sections = glob.glob(pathname=os.path.join(self.__configurations.series_, '**'))

        return [os.path.basename(section) for section in sections]

    def exc(self):
        """

        :return:
        """

        codes = self.__get_sections_codes()

        computations = []
        for code in codes[:2]:
            data = dask.dataframe.read_csv(os.path.join(self.__configurations.series_, code, '**', '*.csv'))
            computations.append(data.compute())
        frame = pd.concat(computations, axis=0)
        logging.info(frame)

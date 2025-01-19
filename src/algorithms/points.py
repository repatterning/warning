"""Module points.py"""
import glob
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

    def __get_sections_codes(self) -> list:
        """
        Devices, therefore time series, of the same catchment area share a parent directory;
        series - {catchment code} - {time series code} - data files per year.<br><br>

        :return: <b>List of distinct catchment codes.</b>
        """

        sections = glob.glob(pathname=os.path.join(self.__configurations.series_, '**'))

        return [os.path.basename(section) for section in sections]

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        codes = self.__get_sections_codes()

        computations = []
        for code in codes[:2]:
            try:
                data = dask.dataframe.read_csv(os.path.join(self.__configurations.series_, code, '**', '*.csv'))
            except ImportError as err:
                raise err from err
            computations.append(data.compute())
        frame = pd.concat(computations, axis=0)

        return frame

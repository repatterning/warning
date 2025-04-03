"""Module seasonal.py"""
import os

import numpy as np
import pandas as pd

import config

import src.functions.objects
import src.elements.specifications as se
import src.elements.parts as pr


class Data:
    """
    <b>Notes</b><br>
    ------<br>

    Retrieves the seasonal component forecasting estimations<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    @staticmethod
    def __get_section(data: dict, section: str) ->pd.DataFrame:
        """

        :param data: A data dictionary of estimations.
        :param section: A data section of the estimations dictionary
        :return:
        """

        frame = pd.DataFrame.from_dict(data[section], orient='tight')

        # sort
        frame.sort_values(by='timestamp', ascending=True, inplace=True)

        return frame

    def exc(self, specifications: se.Specifications) -> pr.Parts:
        """

        :param specifications:
        :return:
        """

        # Reading-in
        uri = os.path.join(self.__configurations.data_, 'models', str(specifications.catchment_id),
                           str(specifications.ts_id), 'estimates.json')
        data = src.functions.objects.Objects().read(uri=uri)

        return pr.Parts(
            training=self.__get_section(data=data, section='training'),
            testing=self.__get_section(data=data, section='testing'),
            futures=self.__get_section(data=data, section='futures'))

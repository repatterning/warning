"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.specifications as se
import src.functions.directories
import src.functions.objects


class Persist:
    """
    <b>Notes</b><br>
    -------<br>

    Structures and saves each institution's drift data.
    """

    def __init__(self):
        """
        Beware, .to_json() will automatically convert the values of a datetime64[] field
        to milliseconds epoch, therefore <milliseconds> ≡ <date>

        """

        self.__fields = ['milliseconds', 'js', 'wasserstein']

        # Instances
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Storage
        self.__path = os.path.join(self.__configurations.points_, 'drift')
        src.functions.directories.Directories().create(self.__path)

    def __get_dictionary(self, frame: pd.DataFrame, specifications: se.Specifications):
        """


        :param frame:
        :return:
        """

        spe = specifications._asdict()
        for value in ['station_id', 'catchment_id', 'ts_id']:
            spe[value] = int(spe.get(value))

        string: str = frame[self.__fields].to_json(orient='split')
        dictionary: dict = json.loads(string)
        dictionary.update(spe)

        return dictionary

    def exc(self, frame: pd.DataFrame, specifications: se.Specifications) -> str:
        """

        :param frame:
        :param specifications:
        :return:
        """

        # Dictionary
        dictionary = self.__get_dictionary(frame=frame, specifications=specifications)

        message = self.__objects.write(
            nodes=dictionary, path=os.path.join(self.__path, f'{specifications.ts_id}.json'))

        return message

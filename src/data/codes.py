"""Module codes.py"""
import glob
import os
import pathlib

import config


class Codes:
    """
    <b>Notes</b><br>
    ------<br>
    Determines the institutions list.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path_m = os.path.join(self.__configurations.data_, 'models')
        self.__path_d = os.path.join(self.__configurations.data_, 'data')

    def __re_cut(self, string: str) -> str:
        """

        :param string: A path string
        :return:
        """

        string = string.rstrip(os.sep)
        values = string.split(sep=os.sep)

        return values[-2] + os.sep + values[-1]

    def __get_codes(self) -> list[str] | None:
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__path_m, '**', '**'))
        stems = [self.__re_cut(listing) for listing in listings]

        codes = []
        for stem in stems:
            state = (pathlib.Path(os.path.join(self.__path_m, stem, 'estimates.json')).exists() &
                     pathlib.Path(os.path.join(self.__path_d, stem, 'data.csv')).exists() &
                     pathlib.Path(os.path.join(self.__path_d, stem, 'training.csv')).exists() &
                     pathlib.Path(os.path.join(self.__path_d, stem, 'testing.csv')).exists())
            if state:
                codes.append(stem)
        return codes

    def exc(self) -> list[str] | None:
        """

        :return:
        """

        return self.__get_codes()

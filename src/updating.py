"""Module data/updating.py"""
import os

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.cache
import src.functions.streams


class Updating:
    """
    Updating
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __update(self, uri: str, frame: pd.DataFrame) -> str:
        """

        :param uri: Storage path.
        :param frame: Warning data
        :return:
        """

        # If the file does not exist, an empty data frame is returned
        text = txa.TextAttributes(uri=uri, header=0)
        original = self.__streams.read(text=text)
        instances = pd.concat([original, frame], axis=0, ignore_index=True)
        instances.drop_duplicates(inplace=True)

        return self.__streams.write(
            blob=instances,
            path=os.path.join(self.__configurations.warehouse, self.__configurations.library_.replace('/', os.sep)))

    def exc(self, frame: pd.DataFrame) -> str:
        """

        :param frame: The data of a gauge.
        :return:
        """

        frame.drop(columns='geometry', inplace=True)
        uri = f's3://{self.__s3_parameters.internal}/{self.__configurations.library_}'

        return self.__update(uri=uri, frame=frame)

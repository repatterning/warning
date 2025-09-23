"""Module data/updating.py"""
import os

import pandas as pd

import config
import src.cartography.metadata
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.elements.text_attributes as txa
import src.functions.cache
import src.functions.directories
import src.functions.streams
import src.s3.upload


class Updating:
    """
    Updating
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        # Instances
        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()
        self.__streams = src.functions.streams.Streams()
        self.__metadata = src.cartography.metadata.Metadata()

    def __update(self, uri: str, frame: pd.DataFrame, affix: str) -> bool:
        """

        :param uri: Storage path.
        :param frame: Warning data
        :param affix:
        :return:
        """

        # If the file does not exist, an empty data frame is returned
        text = txa.TextAttributes(uri=uri, header=0)
        original = self.__streams.read(text=text)
        instances = pd.concat([original, frame], axis=0, ignore_index=True)
        instances.drop_duplicates(inplace=True)

        return src.s3.upload.Upload(
            service=self.__service, s3_parameters=self.__s3_parameters).bytes(
            data=instances, metadata=self.__metadata.metadata, key_name=affix)

    def exc(self, frame: pd.DataFrame) -> str:
        """

        :param frame: The data of a gauge.
        :return:
        """

        affix = 'warning/data.csv'
        uri = f's3://{self.__s3_parameters.internal}/{affix}'

        success = self.__update(uri=uri, frame=frame, affix=affix)
        if success:
            return 'The warnings data library has been updated.'

        src.functions.cache.Cache().exc()
        raise 'Unable to update the warnings data library.'

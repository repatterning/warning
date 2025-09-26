"""Module interface.py"""
import logging
import os

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.transfer.metadata
import src.s3.ingress
import src.transfer.dictionary
import src.transfer.initial


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service,  s3_parameters: s3p):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        self.__metadata = src.transfer.metadata.Metadata().metadata

    def exc(self):
        """

        :return:
        """

        # The strings for transferring data to Amazon S3 (Simple Storage Service)
        dictionary = src.transfer.dictionary.Dictionary()
        strings: pd.DataFrame = dictionary.exc(
            path=os.path.join(os.getcwd(), 'warehouse'), extension='*', prefix='')
        strings['metadata'] = strings['vertex'].apply(lambda x: self.__metadata[os.path.basename(x)])
        logging.info(strings)

        # Transfer
        if not strings.empty:
            src.transfer.initial.Initial(service=self.__service, s3_parameters=self.__s3_parameters).exc()
            messages = src.s3.ingress.Ingress(
                service=self.__service, bucket_name=self.__s3_parameters.internal).exc(
                strings=strings, tagging='project=hydrography')
            logging.info(messages)
        else:
            logging.info('Empty')

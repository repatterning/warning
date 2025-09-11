"""Module algorithms/interface.py"""
import logging

import boto3
import geopandas

import src.cartography.data


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__arguments = arguments

    def exc(self):
        """

        :return:
        """

        data: geopandas.GeoDataFrame = src.cartography.data.Data(
            connector=self.__connector, arguments=self.__arguments).exc()
        data.info()
        logging.info(data)

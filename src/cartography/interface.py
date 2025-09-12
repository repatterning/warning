"""Module algorithms/interface.py"""
import logging

import boto3
import geopandas

import src.cartography.data
import src.cartography.cuttings
import src.cartography.reference
import src.elements.s3_parameters as s3p


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self):
        """

        :return:
        """

        data: geopandas.GeoDataFrame = src.cartography.data.Data(
            connector=self.__connector, arguments=self.__arguments).exc()

        reference: geopandas.GeoDataFrame = src.cartography.reference.Reference(
            s3_parameters=self.__s3_parameters).exc()

        initial = [src.cartography.cuttings.Cuttings(reference=reference).members(_polygon=_polygon)
                   for _polygon in data.geometry]
        logging.info(type(initial))
        logging.info(initial)

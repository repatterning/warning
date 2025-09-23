"""Module algorithms/interface.py"""
import logging
import sys

import boto3
import geopandas
import pandas as pd

import src.cartography.cuttings
import src.cartography.data
import src.cartography.reference
import src.cartography.updating
import src.elements.s3_parameters as s3p
import src.elements.system as stm
import src.elements.service as sr
import src.functions.cache
import src.functions.streams


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, service: sr.Service, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param service:
        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__service = service
        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    @staticmethod
    def __members(data: geopandas.GeoDataFrame, reference: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        """
        Which gauges, if any, lie within a warning area?

        :param data:
        :param reference:
        :return:
        """

        initial: list[geopandas.GeoDataFrame] = [
            src.cartography.cuttings.Cuttings(reference=reference).members(_elements=stm.System._make(_elements))
            for _elements in data.itertuples()]

        if len(initial) == 0:
            logging.info('No warnings')
            src.functions.cache.Cache().exc()
            sys.exit(0)

        return pd.concat(initial, axis=0, ignore_index=True)

    def exc(self):
        """

        :return:
        """

        # The country's gauge assets
        reference: geopandas.GeoDataFrame = src.cartography.reference.Reference(
            s3_parameters=self.__s3_parameters).exc()

        # The latest geo-spatial weather warning data
        data: geopandas.GeoDataFrame = src.cartography.data.Data(
            connector=self.__connector, arguments=self.__arguments).exc()
        data: geopandas.GeoDataFrame = data.to_crs(epsg=int(reference.crs.srs.split(':')[1]))

        # Hence
        frame: geopandas.GeoDataFrame = self.__members(data=data, reference=reference)

        # Update the warnings data library
        message = src.cartography.updating.Updating(
            service=self.__service, s3_parameters=self.__s3_parameters).exc(frame=frame)



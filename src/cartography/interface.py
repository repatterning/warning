"""Module algorithms/interface.py"""
import logging
import sys

import boto3
import geopandas
import pandas as pd

import src.cartography.cuttings
import src.cartography.data
import src.cartography.reference
import src.elements.s3_parameters as s3p
import src.functions.cache
import src.functions.streams


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

    def __persist(self, initial: list[geopandas.GeoDataFrame]):
        """

        :param initial:
        :return:
        """

        frame: geopandas.GeoDataFrame = pd.concat(initial, axis=0, ignore_index=True)
        path = self.__s3_parameters.internal + '/' + self.__s3_parameters.path_internal_data + 'warning/latest.geojson'

        src.functions.streams.Streams().write(blob=frame, path=path)


    def exc(self):
        """

        :return:
        """

        reference: geopandas.GeoDataFrame = src.cartography.reference.Reference(
            s3_parameters=self.__s3_parameters).exc()

        data: geopandas.GeoDataFrame = src.cartography.data.Data(
            connector=self.__connector, arguments=self.__arguments).exc()
        data: geopandas.GeoDataFrame = data.to_crs(epsg=int(reference.crs.srs.split(':')[1]))

        initial: list[geopandas.GeoDataFrame] = [
            src.cartography.cuttings.Cuttings(reference=reference).members(_polygon=_polygon)
            for _polygon in data.geometry]

        if len(initial) == 0:
            logging.info('No warnings')
            src.functions.cache.Cache().exc()
            sys.exit(0)

        self.__persist(initial=initial)

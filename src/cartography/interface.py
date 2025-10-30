"""Module algorithms/interface.py"""
import boto3
import geopandas
import numpy as np

import src.cartography.latest
import src.cartography.members
import src.cartography.reference
import src.cartography.times
import src.cartography.updating
import src.elements.s3_parameters as s3p


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, connector: boto3.session.Session,
                 s3_parameters: s3p.S3Parameters, arguments: dict):
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

    @staticmethod
    def __filtering(data: geopandas.GeoDataFrame):
        """

        :param data:
        :return:
        """

        if sum(data['warning_level'].str.upper() == 'RED') > 0:
            instances = data.copy().loc[data['warning_level'].str.upper() == 'RED', :]
        elif sum(data['warning_level'].str.upper() == 'AMBER') > 0:
            instances = data.copy().loc[data['warning_level'].str.upper() == 'AMBER', :]
        else:
            instances = data.copy()

        return instances

    def __limiting(self, data: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        """

        :param data:
        :return:
        """

        limit = self.__arguments.get('n_catchments_limit')

        catchments = data['catchment_id'].unique()

        if catchments.shape[0] > limit:
            excerpt = np.sort(catchments, axis=-1)[-limit:]
            data = data.copy().loc[data['catchment_id'].isin(excerpt), :]

        return data

    def exc(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        # The country's gauge assets
        reference: geopandas.GeoDataFrame = src.cartography.reference.Reference(
            s3_parameters=self.__s3_parameters).exc()

        # The latest geo-spatial weather warning data
        latest: geopandas.GeoDataFrame = src.cartography.latest.Latest(
            connector=self.__connector, arguments=self.__arguments).exc()

        # Hence
        data: geopandas.GeoDataFrame = src.cartography.members.Members(
            arguments=self.__arguments).exc(latest=latest, reference=reference)
        data = self.__filtering(data=data.copy())
        data = self.__limiting(data=data.copy())

        # Update the warnings data library
        src.cartography.updating.Updating(s3_parameters=self.__s3_parameters).exc(data=data)

        # Times
        src.cartography.times.Times().exc(data=data)

        return data

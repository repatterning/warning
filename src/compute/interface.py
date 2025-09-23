"""Module compute/interface.py"""
import logging
import boto3
import datetime

import geopandas
import pandas as pd

import src.compute.schedule
import src.compute.settings


class Interface:
    """
    The interface to the compute package programs
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__arguments = arguments

    @staticmethod
    def __timestamp(value: pd.Timestamp) -> datetime.datetime:
        """

        :param value:
        :return:
        """

        _st = value.to_pydatetime()

        return datetime.datetime.fromtimestamp(_st.timestamp())

    def exc(self, frame: geopandas.GeoDataFrame):
        """

        :param frame:
        :return:
        """

        starting = self.__timestamp(value = frame['starting'].min())
        ending = self.__timestamp(value = frame['ending'].max())

        settings = src.compute.settings.Settings(
            connector=self.__connector, project_key_name=self.__arguments.get('project_key_name')).exc(
            starting=starting, ending=ending)

        src.compute.schedule.Schedule(connector=self.__connector).create_schedule(settings=settings)

"""Module compute/interface.py"""
import datetime

import boto3
import geopandas
import pandas as pd
import pytz

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

        # Time & Place
        self.__place = pytz.timezone('Europe/Dublin')

    def __timestamp(self, value: pd.Timestamp) -> datetime.datetime:
        """
        zoneinfo.ZoneInfo('Europe/London')

        :param value:
        :return:
        """

        _initial = value.to_pydatetime()
        _free = datetime.datetime.fromtimestamp(_initial.timestamp(), tz=None)

        return self.__place.localize(_free)

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

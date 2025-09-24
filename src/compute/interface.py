"""Module compute/interface.py"""
import datetime
import logging

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
        self.__place.localize(_free)

        :param value:
        :return:
        """

        _initial = value.to_pydatetime()
        _free = datetime.datetime.fromtimestamp(_initial.timestamp(), tz=self.__place)

        return _free

    def exc(self, frame: geopandas.GeoDataFrame):
        """

        :param frame:
        :return:
        """

        # Cloud Compute Times: The data times and the cloud compute times exist within different zones
        starting = self.__timestamp(value = frame['starting'].min())
        ending = self.__timestamp(value = frame['ending'].max())

        # Schedule Settings
        settings = src.compute.settings.Settings(
            connector=self.__connector, project_key_name=self.__arguments.get('project_key_name')).exc(
            starting=starting, ending=ending)

        # Does the schedule exist?
        sch = self.__connector.client(service_name='scheduler')
        try:
            response = sch.get_schedule(
                GroupName=settings.get('group_name'), Name=settings.get('name'))
        except sch.exceptions.ResourceNotFoundException:
            src.compute.schedule.Schedule(
                connector=self.__connector).create_schedule(settings=settings)
        else:
            logging.info('\n\nSCHEDULE:\n%s\n%s\n', response, type(response))

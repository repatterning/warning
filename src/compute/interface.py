"""Module compute/interface.py"""
import logging
import boto3

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

    def exc(self, starting, ending):
        """

        :param starting:
        :param ending:
        :return:
        """

        logging.info(type(starting))
        logging.info(type(ending))

        settings = src.compute.settings.Settings(
            connector=self.__connector, project_key_name=self.__arguments.get('project_key_name')).exc(
            starting=starting, ending=ending)

        src.compute.schedule.Schedule(connector=self.__connector).create_schedule(settings=settings)

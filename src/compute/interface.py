import src.compute.settings
import src.compute.schedule
import boto3


class Interface:

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector:
        :param arguments:
        """

        self.__connector = connector
        self.__arguments = arguments



    def exc(self, starting, ending):

        settings = src.compute.settings.Settings(
            connector=self.__connector, project_key_name=self.__arguments.get('project_key_name')).exc(
            starting=starting, ending=ending)

        src.compute.schedule.Schedule(connector=self.__connector).create_schedule(settings=settings)

"""Module schedule.py"""
import logging

import boto3
import botocore.exceptions


class Schedule:
    """
    Schedule
    """

    def __init__(self, connector: boto3.session.Session):
        """
        Constructor
        """

        # self.__scheduler_client = boto3.client('scheduler')
        self.__scheduler_client = connector.client(service_name='scheduler')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def create_schedule(self, settings: dict) -> str:
        """
        Creates a new schedule with the specified parameters.

        :param settings:
        :return:
            The ARN of the created schedule.
        """
        try:
            parameters = {
                'Name': settings.get('name'),
                'ScheduleExpression': settings.get('schedule_expression'),
                'GroupName': settings.get('group_name'),
                'Target': {'Arn': settings.get('arn'), 'RoleArn': settings.get('role_arn')},
                'StartDate': settings.get('starting'),
                'EndDate': settings.get('ending')}

            if settings.get('delete_after_completion'):
                parameters['ActionAfterCompletion'] = 'DELETE'

            if settings.get('use_flexible_window_time'):
                parameters['FlexibleTimeWindow']['Mode'] = 'FLEXIBLE'
                parameters['FlexibleTimeWindow']['MaximumWindowInMinutes'] = settings.get('maximum_window_in_minutes')
            else:
                parameters['FlexibleTimeWindow']['Mode'] = 'OFF'

            response = self.__scheduler_client.create_schedule(**parameters)

            return response['ScheduleArn']

        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConflictException':
                self.__logger.error('Failed to create schedule %s: %s', settings.get('name'), err.response['Error']['Message'])
            else:
                self.__logger.error('Error creating schedule: %s', err.response['Error']['Message'])
            raise

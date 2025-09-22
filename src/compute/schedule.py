"""Module schedule.py"""
import logging

import boto3
import botocore.exceptions


class Schedule:

    def __init__(self):
        """
        Constructor
        """

        self.__scheduler_client = boto3.client('scheduler')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def create_schedule(self, arguments: dict) -> str:
        """
        Creates a new schedule with the specified parameters.

        :param arguments:
        :return:
            The ARN of the created schedule.
        """
        try:
            parameters = {
                'Name': arguments.get('name'),
                'ScheduleExpression': arguments.get('schedule_expression'),
                'GroupName': arguments.get('group_name'),
                'Target': {'Arn': arguments.get('arn'), 'RoleArn': arguments.get('role_arn')},
                'StartDate': arguments.get('starting'),
                'EndDate': arguments.get('ending')}

            if arguments.get('delete_after_completion'):
                parameters['ActionAfterCompletion'] = 'DELETE'

            if arguments.get('use_flexible_window_time'):
                parameters['FlexibleTimeWindow']['Mode'] = 'FLEXIBLE'
                parameters['FlexibleTimeWindow']['MaximumWindowInMinutes'] = arguments.get('maximum_window_in_minutes')
            else:
                parameters['FlexibleTimeWindow']['Mode'] = 'OFF'

            response = self.__scheduler_client.create_schedule(**parameters)

            return response['ScheduleArn']

        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConflictException':
                self.__logger.error('Failed to create schedule %s: %s', arguments.get('name'), err.response['Error']['Message'])
            else:
                self.__logger.error('Error creating schedule: %s', err.response['Error']['Message'])
            raise

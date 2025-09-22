
import logging

import datetime
import boto3
import botocore.exceptions


class Schedule:

    def __init__(self):

        self.__scheduler_client = boto3.client('scheduler')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def create_schedule(self, name: str, schedule_expression: str, schedule_group_name: str, target_arn: str, role_arn: str,
                        target_input: str, delete_after_completion: bool = False, use_flexible_time_window: bool = False,
    ) -> str:
        """
        Creates a new schedule with the specified parameters.

        :param name: The name of the schedule.
        :param schedule_expression: The expression that defines when the schedule runs.
        :param schedule_group_name: The name of the schedule group.
        :param target_arn: The Amazon Resource Name (ARN) of the target.
        :param role_arn: The Amazon Resource Name (ARN) of the execution IAM role.
        :param target_input: The target_input for the target.
        :param delete_after_completion: Whether to delete the schedule after it completes.
        :param use_flexible_time_window: Whether to use a flexible time window.

        :return The ARN of the created schedule.
        """
        try:
            hours_to_run = 60
            flexible_time_window_minutes = int(5)
            parameters = {
                'Name': name,
                'ScheduleExpression': schedule_expression,
                'GroupName': schedule_group_name,
                'Target': {'Arn': target_arn, 'RoleArn': role_arn, 'Input': target_input},
                'StartDate': datetime.datetime.now(datetime.timezone.utc),
                'EndDate': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours_to_run)}

            if delete_after_completion:
                parameters['ActionAfterCompletion'] = 'DELETE'

            if use_flexible_time_window:
                parameters['FlexibleTimeWindow']['Mode'] = 'FLEXIBLE'
                parameters['FlexibleTimeWindow']['MaximumWindowInMinutes'] = flexible_time_window_minutes
            else:
                parameters['FlexibleTimeWindow']['Mode'] = 'OFF'

            response = self.__scheduler_client.create_schedule(**parameters)

            return response['ScheduleArn']
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConflictException':
                self.__logger.error('Failed to create schedule %s: %s', name, err.response['Error']['Message'])
            else:
                self.__logger.error('Error creating schedule: %s', err.response['Error']['Message'])
            raise
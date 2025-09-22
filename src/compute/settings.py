"""Module settings.py"""
import datetime

import boto3

import src.functions.secret


class Settings:
    """
    Creates a schedule's dictionary of arguments.
    """

    def __init__(self, connector: boto3.session.Session, project_key_name: str):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__project_key_name = project_key_name

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)

    def exc(self, starting: datetime.datetime, ending: datetime.datetime) -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule.html

        :param starting: The start time
        :param ending: The end time
        :return:
        """

        '''
        :param name: The schedule's name.
        :param schedule_expression: The timing schedule.
        :param group_name: The name of the schedule group.
        :param arn: The Amazon Resource Name (ARN) of the target.
        :param role_arn: The Amazon Resource Name (ARN) of the execution IAM role.
        :param delete_after_completion: Whether to delete the schedule after it completes.
        :param use_flexible_time_window: Whether to use a flexible time window.
        :param maximum_window_in_minutes: The span of the afore flexible time window.
        '''
        arguments = {
            'name': 'HydrographyWarningSystem',
            'schedule_expression': 'rate(2 hours)',
            'starting': starting,
            'ending': ending,
            'group_name': 'default',
            'arn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-arn-warning-system'),
            'role_arn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-execution-role-arn'),
            'delete_after_completion': True,
            'use_flexible_window_time': True,
            'maximum_window_in_minutes': 5
        }

        return arguments

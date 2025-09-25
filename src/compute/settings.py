"""Module settings.py"""
import datetime

import boto3

import src.functions.secret


class Settings:
    """
    Creates a schedule's dictionary of arguments.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__project_key_name = arguments.get('project_key_name')

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)

        self.__scheduler: dict = arguments.get('scheduler')

    def exc(self, starting: datetime.datetime, ending: datetime.datetime) -> dict:
        """
        For more about a schedule's parameters & arguments visit
        <a
        href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule.html"
        target="_blank">EventBridgeScheduler.Client.create_schedule()</a><br><br>

        name: The schedule's name.<br>
        schedule_expression: The timing schedule.<br>
        group_name: The name of the schedule group.<br>
        arn: The Amazon Resource Name (ARN) of the target.<br>
        role_arn: The Amazon Resource Name (ARN) of the execution IAM role.<br>
        delete_after_completion: Whether to delete the schedule after it completes.<br>
        use_flexible_time_window: Whether to use a flexible time window.<br>
        maximum_window_in_minutes: The span of the afore flexible time window.<br><br>

        :param starting: The start time
        :param ending: The end time<br>
        :return:
        """

        settings = {
            'Name': self.__scheduler.get('name'),
            'ScheduleExpression': self.__scheduler.get('schedule_expression'),
            'ScheduleExpressionTimezone': self.__scheduler.get('schedule_expression_timezone'),
            'StartDate': starting,
            'EndDate': ending,
            'GroupName': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-group'),
            'Target': {
                'Arn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-arn-warning-system'),
                'RoleArn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-execution-role-arn'),
                'RetryPolicy': {
                    'MaximumEventAgeInSeconds': self.__scheduler.get(
                        'target').get('retry_policy').get('maximum_event_age_in_seconds'),
                    'MaximumRetryAttempts': self.__scheduler.get(
                        'target').get('retry_policy').get('maximum_retry_attempts')
                }
            },
            'ActionAfterCompletion': self.__scheduler.get('action_after_completion'),
            'FlexibleTimeWindow': {
                'Mode': self.__scheduler.get('flexible_time_window').get('mode'),
                'MaximumWindowInMinutes': self.__scheduler.get('flexible_time_window').get('maximum_window_in_minutes')
            }
        }

        return settings

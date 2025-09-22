"""Module settings.py"""
import datetime

import boto3

import src.functions.secret


class Settings:
    """
    Builds the ...
    """

    def __init__(self, connector: boto3.session.Session, project_key_name: str):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__project_key_name = project_key_name

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)

    def exc(self, starting: datetime.datetime, ending: datetime.datetime):

        elements = {
            'name': 'HydrographyWarningSystem',
            'starting': starting,
            'ending': ending,
            'group_name': 'default',
            'arn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-arn-warning-system'),
            'role_arn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-execution-role-arn'),
            'delete_after_completion': True,
            'use_flexible_window_time': True,
            'maximum_window_in_minutes': 5
        }

        return elements

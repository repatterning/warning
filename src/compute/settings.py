import boto3

import src.functions.secret



class Settings:

    def __init__(self, connector: boto3.session.Session, project_key_name: str):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__project_key_name = project_key_name

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)


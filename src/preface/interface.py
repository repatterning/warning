"""Module interface.py"""
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __get_arguments(self, connector: boto3.session.Session) -> dict:
        """

        :return:
        """

        key_name = self.__configurations.argument_key

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()

        # Arguments
        arguments: dict = self.__get_arguments(connector=connector)

        # Interaction Instances: Amazon
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(
            connector=connector, project_key_name=arguments.get('project_key_name')).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()

        src.preface.setup.Setup().exc()

        return connector, s3_parameters, service, arguments

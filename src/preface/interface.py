"""Module interface.py"""
import sys
import typing

import boto3

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
        pass

    @staticmethod
    def __get_arguments(connector: boto3.session.Session) -> dict:
        """

        :return:
        """

        key_name = 'artefacts' + '/' + 'architecture' + '/' + 'autoregressive' + '/' + 'arguments.json'

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        arguments: dict = self.__get_arguments(connector=connector)

        setup = src.preface.setup.Setup().exc()
        if setup:
            return connector, s3_parameters, service, arguments

        src.functions.cache.Cache().exc()
        sys.exit('Unable to set up local environments.')

import logging

import boto3
import xml.etree.ElementTree as et
import requests

import src.functions.secret


class Interface:

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector:
        :param arguments:
        """

        self.__connector = connector
        self.__arguments = arguments

        self.__secret = src.functions.secret.Secret(connector=self.__connector)

        # self.__endpoint = 'https://{key}/v1.0/objects/feed'
        self.__url = 'https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/feed'

    def exc(self):



        key = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'), node='nswws')

        headers = {
            'x-API-key': key
        }

        response = requests.get(url=self.__url, headers=headers)

        logging.info(response.status_code)
        logging.info(response.headers)
        logging.info(response.content)

        page = et.fromstring(response.content)
        logging.info(page)

        for part in page:
            logging.info(part)




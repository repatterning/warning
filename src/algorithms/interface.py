"""Module algorithms/interface.py"""
import logging
import xml.etree.ElementTree as et

import boto3
import requests
import io
import geopandas

import src.functions.secret


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__arguments = arguments

        self.__secret = src.functions.secret.Secret(connector=self.__connector)

        #
        self.__url = 'https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/feed'

    def __data(self, page: et.Element, headers: dict) -> geopandas.GeoDataFrame:

        frame = geopandas.GeoDataFrame()
        for paragraph in page.findall('{http://www.w3.org/2005/Atom}link'):

            elements = paragraph.attrib
            if elements.get('type') == 'application/vnd.geo+json':
                bits = requests.get(url=elements.get('href'), headers=headers)
                frame = geopandas.read_file(io.BytesIO(bits.content))

        return frame

    def exc(self):
        """

        :return:
        """

        # Retrieve the service key, and set up the header
        key = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'), node='nswws')
        headers = {
            'x-API-key': key
        }

        response = requests.get(url=self.__url, headers=headers)
        page: et.Element = et.fromstring(response.content)
        data = self.__data(page=page, headers=headers)
        logging.info(data.empty)
        logging.info(data)

"""Module algorithms/interface.py"""
import io
import logging
import os.path
import sys
import xml.etree.ElementTree as  et

import boto3
import geopandas
import pandas as pd
import requests

import config
import src.functions.cache
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

        self.__configurations = config.Config()
        self.__secret = src.functions.secret.Secret(connector=self.__connector)

    def __data(self, page: et.Element, headers: dict) -> geopandas.GeoDataFrame:
        """
        requests.get(..., timeout -> seconds)

        :param page: An Atom Feed.  It outlines the latest set of weather warnings, and updates of the warnings, including
                     cancellations and expirations; <a href="https://metoffice.github.io/nswws-public-api/atom-feed.html">
                     continue reading</a>.
        :param headers: For retrieving web data.
        :return:
        """

        computations = []
        frame = geopandas.GeoDataFrame()
        for paragraph in page.findall('{http://www.w3.org/2005/Atom}link'):
            elements = paragraph.attrib
            if elements.get('type') == 'application/vnd.geo+json':
                bits = requests.get(url=elements.get('href'), headers=headers, timeout=30)
                part = geopandas.read_file(io.BytesIO(bits.content))
                computations.append(part)

        frame = frame if len(computations) == 0 else pd.concat(computations, axis=0, ignore_index=True)

        return frame

    def __temporary(self) -> geopandas.GeoDataFrame:

        try:
            return geopandas.read_file(
                filename=os.path.join(self.__configurations.data_, 'latest.geojson'))
        except FileNotFoundError as err:
            raise err from err

    def exc(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        # Retrieve the service key, and set up the header
        key = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'), node='nswws')
        url = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'), node='nswws-base')
        headers = {
            'x-API-key': key
        }

        # Retrieve the XML Feed; time out -> seconds
        response = requests.get(url=url, headers=headers, timeout=30)
        logging.info(response.content)
        page: et.Element = et.fromstring(response.content)

        # get geojson data
        data = self.__data(page=page, headers=headers)

        if data.empty:
            logging.info('no warnings')
            src.functions.cache.Cache().exc()
            sys.exit()

        return data

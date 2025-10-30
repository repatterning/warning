
import logging
import datetime
import uuid

import geopandas
import pytz

import config


class Temporary:

    def __init__(self):
        """
        Constructor
        """

        self.__minutes = 16

        # Instances
        self.__configurations = config.Config()

    def __call__(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        baseline = datetime.datetime.now(pytz.utc)

        try:
            frame = geopandas.read_file(
                filename=self.__configurations.area_)
            frame['warningId'] = str(uuid.uuid4())
            frame['validFromDate'] = baseline + datetime.timedelta(minutes=self.__minutes)
            frame['validToDate'] = baseline + datetime.timedelta(minutes=2*self.__minutes)
            logging.info(frame)
            return frame
        except FileNotFoundError as err:
            raise err from err

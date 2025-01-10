"""Module points.py"""
import logging

import pandas as pd

import src.functions.objects


class Points:
    """
    <b>Notes</b><br>
    ------<br>
    """

    def __init__(self, pilot: pd.DataFrame):
        """

        :param pilot:
        """

        self.__pilot = pilot

        self.__objects = src.functions.objects.Objects()

        self.__url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
                      '&request=getTimeseriesValues&ts_id={ts_id}&period={period}&from={datestr}'
                      '&returnfields=Timestamp,Value,Quality Code&metadata=true'
                      '&md_returnfields=ts_id,ts_name,ts_unitname,ts_unitsymbol,station_id,'
                      'catchment_id,parametertype_id,parametertype_name,river_name&dateformat=UNIX&format=json')

    def exc(self, ts_id: int, period: str, datestr: str):
        """
        P1D, P1M, etc.

        :param ts_id: A time series identification code
        :param period: The period of time of interest.
        :param datestr: A yyyy-mm-dd string.
        :return:
        """

        url = self.__url.format(ts_id=ts_id, period=period, datestr=datestr)
        blob = self.__objects.api(url=url)
        logging.info(blob[0])

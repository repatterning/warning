"""Module points.py"""
import logging

import config
import src.elements.partitions as prt
import src.functions.objects


class Points:
    """
    <b>Notes</b><br>
    ------<br>

    Retrieves time series points.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        self.__objects = src.functions.objects.Objects()

        self.__url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
                      '&request=getTimeseriesValues&ts_id={ts_id}'
                      f'&period={self.__configurations.period}'
                      '&from={datestr}&returnfields=Timestamp,Value,Quality Code&metadata=true'
                      '&md_returnfields=ts_id,ts_name,ts_unitname,ts_unitsymbol,station_id,'
                      'catchment_id,parametertype_id,parametertype_name,river_name&dateformat=UNIX&format=json')

    def exc(self, partitions: list[prt.Partitions]):
        """

        :param partitions: ts_id, datestr, catchment_size, gauge_datum, on_river
        :return:
        """

        for partition in partitions:

            url = self.__url.format(ts_id=partition.ts_id, datestr=partition.datestr)
            logging.info(url)
            # blob = self.__objects.api(url=url)
            # logging.info(blob[0])

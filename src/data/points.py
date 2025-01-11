"""Module points.py"""
import logging
import pandas as pd
import dask

import config
import src.elements.partitions as prt
import src.functions.objects


class Points:
    """
    <b>Notes</b><br>
    ------<br>

    The time series data.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # The uniform resource locator, data columns, etc.
        self.__url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
                      '&request=getTimeseriesValues&ts_id={ts_id}'
                      f'&period={self.__configurations.period}'
                      '&from={datestr}&returnfields=Timestamp,Value,Quality Code&metadata=true'
                      '&md_returnfields=ts_id,ts_name,ts_unitname,ts_unitsymbol,station_id,'
                      'catchment_id,parametertype_id,parametertype_name,river_name&dateformat=UNIX&format=json')

        self.__rename = {'Timestamp': 'timestamp', 'Value': 'value', 'Quality Code': 'quality_code'}

    @dask.delayed
    def __get_data(self, url: str):
        """

        :param url:
        :return:
        """

        parts = self.__objects.api(url=url)

        # The data in data frame form
        columns = parts[0]['columns'].split(',')
        frame = pd.DataFrame.from_records(data=parts[0]['data'], columns=columns)
        frame.rename(columns=self.__rename, inplace=True)

        # The identification codes of the time series
        frame = frame.assign(
            station_id=parts[0]['station_id'], catchment_id=parts[0]['catchment_id'])

        return frame

    @dask.delayed
    def __extra_features(self, data: pd.DataFrame, partition: prt.Partitions):
        """

        :param data:
        :param partition:
        :return:
        """

        data = data.assign(
            catchment_size=partition.catchment_size, gauge_datum=partition.gauge_datum, on_river=int(partition.on_river))

        return data

    @dask.delayed
    def __persist(self, data: pd.DataFrame, partition: prt.Partitions) -> str:

        logging.info(data.head())

        return f'{partition.ts_id}: {partition.datestr}'

    def exc(self, partitions: list[prt.Partitions]):
        """

        :param partitions: ts_id, datestr, catchment_size, gauge_datum, on_river
        :return:
        """

        computations = []
        for partition in partitions:

            url = self.__url.format(ts_id=partition.ts_id, datestr=partition.datestr)
            data = self.__get_data(url=url)
            data = self.__extra_features(data=data.copy(), partition=partition)
            message = self.__persist(data=data, partition=partition)

            computations.append(message)
        calculations = dask.compute(computations, scheduler='threads')[0]

        logging.info(calculations)

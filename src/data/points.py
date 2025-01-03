import logging
import src.functions.objects


class Points:

    def __init__(self):

        self.__objects = src.functions.objects.Objects()

    def exc(self):

        url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices'
               '&datasource=0&request=getTimeseriesValues&ts_path=1/*/SG/15m.Cmd'
               '&period=P7D&returnfields=Timestamp,Value,Quality%20Code&format=json')

        blob = self.__objects.api(url=url)

        logging.info(blob)

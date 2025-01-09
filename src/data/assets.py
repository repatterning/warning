
import pandas as pd

class Assets:

    def __init__(self, codes: pd.DataFrame, stations: pd.DataFrame):

        self.__codes = codes
        self.__stations = stations

    def __get_instances(self) -> pd.DataFrame:

        left = ['station_id', 'catchment_id', 'stationparameter_no', 'parametertype_id', 'ts_id', 'ts_name', 'from', 'to']
        right = ['station_id', 'station_latitude', 'station_longitude', 'river_id',
                 'CATCHMENT_SIZE', 'GAUGE_DATUM', 'GROUND_DATUM']

        data = self.__codes[left].merge(self.__stations[right], on='station_id', how='left')

        return data

    def __coordinates(self, instances: pd.DataFrame) -> pd.DataFrame:
        pass

    def exc(self):

        instances = self.__get_instances()
        
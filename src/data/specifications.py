
import pandas as pd

import src.elements.specifications as se


class Specifications:

    def __init__(self):
        pass

    def __anomalies(self, specifications: se.Specifications) -> se.Specifications:
        """

        :param specifications:
        :return:
        """

        specifications = specifications._replace(catchment_id=int(specifications.catchment_id),
                                                 station_id=int(specifications.station_id),
                                                 ts_id=int(specifications.ts_id))

        return specifications

    def exc(self, reference: pd.DataFrame) -> list[se.Specifications]:

        dictionaries = [reference.iloc[i, :].squeeze() for i in range(reference.shape[0])]

        specifications_ = [se.Specifications(**dictionary) for dictionary in dictionaries]
        specifications_ = [self.__anomalies(specifications=specifications)
                           for specifications in specifications_]

        return specifications_

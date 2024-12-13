
import os
import logging

import pandas as pd
import numpy as np

import config
import src.functions.streams

class Interface:

    def __init__(self):

        self.__configurations = config.Config()

        self.__streams = src.functions.streams.Streams()

    def __persist(self, blob: pd.DataFrame, path: str):

        return self.__streams.write(blob=blob, path=path)

    def exc(self, architecture: str):

        abscissae = np.linspace(start=0, stop=1, num=101)
        ordinates = np.power(2, abscissae)
        data = pd.DataFrame(data={'abscissa': abscissae, 'ordinate': ordinates})

        path = os.path.join(self.__configurations.storage, f'{architecture}.csv')
        message = self.__persist(blob=data, path=path)

        logging.info(message)

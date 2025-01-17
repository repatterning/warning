import glob
import logging
import os

import numpy as np

import config


class Points:

    def __init__(self):

        self.__configurations = config.Config()

    def exc(self):

        listings = glob.glob(pathname=os.path.join(self.__configurations.series_, '**', '*.csv'), recursive=True)
        logging.info(listings)

        extract = [listings[i] for i in np.arange(len(listings))
                   if listings[i].__contains__('277183') or listings[i].__contains__('277185')]
        logging.info(extract)

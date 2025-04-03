"""Module src.predictions.interface.py"""
import logging
import os

import dask

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.directories
import src.predictions.data
import src.predictions.estimates
import src.predictions.metrics


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __directories(self):
        """

        :return:
        """

        directories = src.functions.directories.Directories()

        for section in ['predictions', 'errors']:
            path = os.path.join(self.__configurations.points_, section)
            directories.create(path)


    def exc(self, specifications_: list[se.Specifications]):
        """

        :param specifications_:
        :return:
        """

        self.__directories()

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_estimates = dask.delayed(src.predictions.estimates.Estimates().exc)
        __get_metrics = dask.delayed(src.predictions.metrics.Metrics().exc)

        computations = []
        for specifications in specifications_:

            parts: pr.Parts = __get_data(specifications=specifications)
            parts_ = __get_estimates(parts=parts, specifications=specifications)
            message_m = __get_metrics(parts=parts_, specifications=specifications)
            computations.append(message_m)

        messages = dask.compute(computations, scheduler='threads', num_workers=6)[0]
        logging.info(messages)

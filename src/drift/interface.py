"""Module interface.py"""
import logging
import os

import dask
import pandas as pd

import config
import src.drift.hankel
import src.drift.metrics
import src.drift.persist
import src.elements.specifications as se
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    <b>Notes</b><br>
    ------<br>
    The interface to drift score programs.<br>
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__arguments = arguments

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    @dask.delayed
    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: The uniform resource identifier of an institution's raw attendances data
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)
        frame = self.__streams.read(text=text)

        frame['date'] = pd.to_datetime(
            frame['date'].astype(str), errors='coerce', format='%Y-%m-%d %H:%M:%S')

        return frame

    def exc(self, specifications_: list[se.Specifications]):
        """

        :param specifications_: List of ...
        :return:
        """

        path = os.path.join(self.__configurations.data_, 'data', '{catchment_id}', '{ts_id}', 'data.csv')

        # Delayed Functions
        hankel = dask.delayed(src.drift.hankel.Hankel(arguments=self.__arguments).exc)
        metrics = dask.delayed(src.drift.metrics.Metrics(arguments=self.__arguments).exc)
        persist = dask.delayed(src.drift.persist.Persist().exc)

        # Compute
        computations = []
        for specifications in specifications_:
            data = self.__get_data(uri=path.format(catchment_id=specifications.catchment_id, ts_id=specifications.ts_id))
            matrix = hankel(data=data)
            frame = metrics(matrix=matrix, data=data)
            message = persist(frame=frame, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads', num_workers=6)[0]
        logging.info('Drift -> \n%s', messages)

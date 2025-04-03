"""Module boundaries.py"""
import json
import logging
import os

import numpy as np
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Estimates:
    """
    <b>Notes</b><br>
    ------<br>
    This class calculates element errors.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'predictions')

        self.__objects = src.functions.objects.Objects()

    @staticmethod
    def __get_errors(data: pd.DataFrame) -> pd.DataFrame:
        """
        data['measure'].to_numpy()[:,None]

        :param data:
        :return:
        """

        data.loc[:, ['error', 'error_l', 'error_u']] = data[['mean', 'mean_ci_lower', 'mean_ci_upper']] - data['measure']
        data['p_error'] = 100*np.true_divide(data['error'].to_numpy(), data['measure'].to_numpy())

        return data

    @staticmethod
    def __get_node(blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        string: str = blob.to_json(orient='split')

        return json.loads(string)

    def __persist(self, nodes: dict, name: str) -> None:
        """

        :param nodes:
        :param name:
        :return:
        """

        message =  self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{name}.json'))
        logging.info(message)

    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> pr.Parts:
        """

        :param parts:
        :param specifications:
        :return:
        """

        training = self.__get_errors(data=parts.training.copy())
        testing = self.__get_errors(data=parts.testing.copy())
        parts = parts._replace(training=training, testing=testing)

        nodes = {
            'training': self.__get_node(parts.training),
            'testing': self.__get_node(parts.testing),
            'futures': parts.futures.to_dict(orient='split')}

        spe = specifications._asdict()
        # for value in ['station_id', 'catchment_id', 'ts_id']:
        #     spe[value] = int(spe.get(value))
        nodes.update(spe)
        self.__persist(nodes=nodes, name=str(specifications.ts_id))

        return parts

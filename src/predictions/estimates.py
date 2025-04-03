"""Module boundaries.py"""
import numpy as np
import pandas as pd
import scipy.stats as sta

import src.elements.parts as pr


class Errors:
    """
    <b>Notes</b><br>
    ------<br>
    This class calculates element errors.<br>
    """

    def __init__(self):
        """
        Constructor
        """

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

    def exc(self, parts: pr.Parts) -> pr.Parts:
        """

        :param parts:
        :return:
        """

        training = self.__get_errors(data=parts.training.copy())
        testing = self.__get_errors(data=parts.testing.copy())


        parts = parts._replace(training=training, testing=testing)

        return parts
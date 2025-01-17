
import pymc

class Design:
    """
    Builds design matrices vis-a-vis lag.
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(lag_coefficients, n_equations, n_lags, frame):
        """

        :param lag_coefficients:
        :param n_equations:
        :param n_lags:
        :param frame:
        :return:
        """

        computations = []
        for j in range(n_equations):
            
            vector = pymc.math.sum(
                [
                    pymc.math.sum(lag_coefficients[j, i] * frame.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                    for i in range(n_lags)
                ],
                axis=0,
            )
    
            computations.append(vector)
            
        beta = pymc.math.stack(computations, axis=-1)
    
        return beta

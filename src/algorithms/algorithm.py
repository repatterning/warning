import numpy as np
import pandas as pd
import pymc
import pymc.distributions


class Algorithm:

    def __init__(self):
        pass

    # noinspection PyTypeChecker
    @staticmethod
    def exc(n_lags: int, n_equations: int, frame: pd.DataFrame, groupings: list, _priors: bool = True):
        
        cols = [col for col in frame.columns if col not in groupings]
        coords = {"lags": np.arange(n_lags) + 1, "equations": cols, "cross_vars": cols}
    
        groups = frame[groupings].drop_duplicates()
    
        with pymc.Model(coords=coords) as model:

            # Hierarchical Priors
            rho = pymc.Beta("rho", alpha=2, beta=2)
            alpha_hat_location = pymc.Normal("alpha_hat_location", 0, 0.1)
            alpha_hat_scale = pymc.InverseGamma("alpha_hat_scale", 3, 0.5)
            beta_hat_location = pymc.Normal("beta_hat_location", 0, 0.1)
            beta_hat_scale = pymc.InverseGamma("beta_hat_scale", 3, 0.5)
            omega_global, _, _ = pymc.LKJCholeskyCov(
                "omega_global", n=n_equations, eta=1.0, sd_dist=pymc.distributions.Exponential.dist(1)
            )

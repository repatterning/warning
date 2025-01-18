"""Module algorithm.py"""
import numpy as np
import pandas as pd
import pymc
import pymc.distributions

import src.algorithms.design


class Algorithm:
    """
    The prospective model's algorithm
    """

    def __init__(self):

        self.__design = src.algorithms.design.Design()

    def exc(self, n_lags: int, n_equations: int, frame: pd.DataFrame, groupings: str, _priors: bool = True):
        """

        :param n_lags:
        :param n_equations:
        :param frame:
        :param groupings:
        :param _priors:
        :return:
        """
        
        cols = [col for col in frame.columns if col not in groupings]
        coords = {"lags": np.arange(n_lags) + 1, "equations": cols, "cross_vars": cols}
    
        groups = frame[groupings].unique()
    
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

            for group in groups:
                
                segment = frame[frame[groupings] == group][cols]
                z_scale_beta = pymc.InverseGamma(f"z_scale_beta_{group}", 3, 0.5)
                z_scale_alpha = pymc.InverseGamma(f"z_scale_alpha_{group}", 3, 0.5)
                lag_coefficients = pymc.Normal(
                    f"lag_coefs_{group}",
                    mu=beta_hat_location,
                    sigma=(beta_hat_scale * z_scale_beta),
                    dims=["equations", "lags", "cross_vars"],
                )
                alpha = pymc.Normal(
                    f"alpha_{group}",
                    mu=alpha_hat_location,
                    sigma=(alpha_hat_scale * z_scale_alpha),
                    dims=("equations",),
                )

                # Homogeneous terms
                h_terms = self.__design(lag_coefficients=lag_coefficients, n_equations=n_equations, n_lags=n_lags, segment=segment)
                h_terms = pymc.Deterministic(f"betaX_{group}", h_terms)
                mean = (alpha + h_terms)

                n = segment.shape[1]
                noise_cholesky, _, _ = pymc.LKJCholeskyCov(
                    f"noise_cholesky_{group}", eta=10, n=n, sd_dist=pymc.distributions.Exponential.dist(1)
                )
                omega = pymc.Deterministic(f"omega_{group}", (rho * omega_global) + ((1 - rho) * noise_cholesky))
                obs = pymc.MvNormal(f"obs_{group}", mu=mean, chol=omega, observed=segment.values[n_lags:])

            if _priors:
                idata = pymc.sample_prior_predictive()
                return model, idata
            else:
                idata = pymc.sample_prior_predictive()
                idata.extend(pymc.sampling.jax.sample_blackjax_nuts(2000, random_seed=120))
                pymc.sample_posterior_predictive(idata, extend_inferencedata=True)

        return model, idata

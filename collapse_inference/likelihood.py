import numpy as np

def likelihood(S_obs, S_model, sigma):
    """
    ℒ: Computes the log-likelihood assuming Gaussian errors.

    Parameters:
    - S_obs: observed data (scalar or array)
    - S_model: predicted model output (same shape as S_obs)
    - sigma: measurement uncertainties (same shape as S_obs)

    Returns:
    - log-likelihood value
    """
    chi2 = np.sum(((S_obs - S_model) / sigma)**2)
    logL = -0.5 * chi2
    return logL

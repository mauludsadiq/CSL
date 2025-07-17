import numpy as np

def collapse_time(S_obs, times, t0):
    """
    ψ′: Collapses the time dimension by selecting the closest observation to t0.

    Parameters:
    - S_obs: array of observations over time
    - times: array of time points (e.g., redshifts)
    - t0: reference time/redshift to collapse to

    Returns:
    - S_collapsed: observation at closest time to t0
    - idx_t0: index of closest time point
    """
    idx_t0 = np.argmin(np.abs(times - t0))  # find closest time to t0
    S_collapsed = S_obs[idx_t0]
    return S_collapsed, idx_t0

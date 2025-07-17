#!/usr/bin/env python3
import numpy as np
import emcee

# Basic settings
ndim = 3            # H0, Omega_m, fR0
nwalkers = 50
nsteps = 10000
nchains = 4         # number of independent chains

def log_prob_fn(params):
    # Replace this with your real likelihood + prior
    H0, Om, fR0 = params
    if not (50 < H0 < 100) or not (0 < Om < 1) or not (-0.5 < fR0 < 0.5):
        return -np.inf
    return -0.5*((H0-74)/5)**2 - 0.5*((Om-0.3)/0.1)**2 - 0.5*(fR0/0.07)**2

all_chains = []

for chain_id in range(nchains):
    print(f"Running chain {chain_id}...")
    p0 = np.random.uniform([60, 0.1, -0.2], [90, 0.5, 0.2], size=(nwalkers, ndim))
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob_fn)
    sampler.run_mcmc(p0, nsteps, progress=True)
    samples = sampler.get_chain(flat=True)
    ids = np.full((samples.shape[0], 1), chain_id)
    samples_with_id = np.hstack([samples, ids])
    all_chains.append(samples_with_id)

merged = np.vstack(all_chains)
np.savetxt("mcmc_multi_chain.csv", merged, delimiter=",")
print("✅ All chains finished. Saved as mcmc_multi_chain.csv")

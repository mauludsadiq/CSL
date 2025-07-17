import numpy as np

# Generate example custom P(k) data
kvals = np.logspace(-4, 0, 200)  # from 10^-4 to 1 Mpc^-1
pkvals = 2e-9 * (kvals/0.05)**0.9  # power spectrum with n_s=0.9

# Save to disk for your CAMB script to read later
np.save('kvals.npy', kvals)
np.save('pkvals.npy', pkvals)

print("Saved kvals.npy and pkvals.npy in cosmo_transfer folder.")

import numpy as np

# Create k-range similar to real BOSS DR12 measurements
k_vals = np.logspace(-2, 0, 25)  # 0.01 to 1.0 h/Mpc

# Model a reasonable P(k): declining power-law shape with scatter
pk_vals = 10000 * (k_vals/0.1)**-1.5
noise = np.random.normal(0, 0.1, len(pk_vals))
pk_vals *= (1 + noise)

# Assign 10% errors
pk_err = 0.1 * pk_vals

# Combine columns
boss_data = np.column_stack([k_vals, pk_vals, pk_err])

# Save in realistic BOSS format
np.savetxt('pk_DR12CMASS_North_z0.57.txt', boss_data,
           fmt='%.6e',
           header='k[h/Mpc]    P(k)[h^-3Mpc^3]    error_P(k)',
           comments='')

print("✅ Saved synthetic BOSS-like P(k) to pk_DR12CMASS_North_z0.57.txt")

import numpy as np

def model(theta, z):
    """
    φ′: Maps parameters theta to model prediction at redshift z.
    Uses a simple flat ΛCDM approximation.
    
    Parameters:
    - theta: array-like [H0, Omega_m, fR0]
    - z: redshift
    
    Returns:
    - d_L: luminosity distance in Mpc
    """
    H0, Omega_m, fR0 = theta  # fR0 is placeholder for future f(R) extension
    E = np.sqrt(Omega_m * (1 + z)**3 + (1 - Omega_m))  # E(z)
    
    dz = np.linspace(0, z, 1000)  # integration grid from 0 to z
    Ez = np.sqrt(Omega_m * (1 + dz)**3 + (1 - Omega_m))
    integral = np.trapz(1/Ez, dz)  # integrate 1/E(z) dz
    
    d_L = (3e5 / H0) * (1 + z) * integral  # luminosity distance in Mpc
    return d_L

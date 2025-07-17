import camb
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# ----------------------------------------
# 1️⃣ Load Planck TT binned data
# ----------------------------------------
planck_data = np.loadtxt('COM_PowerSpect_CMB-TT-binned_R3.01.txt', skiprows=1)
obs_ell = planck_data[:,0]
obs_dl = planck_data[:,1]
obs_err = planck_data[:,3]

print(f"✅ Loaded {len(obs_ell)} Planck binned TT data points.")

# ----------------------------------------
# 2️⃣ Load synthetic BOSS P(k) data
# ----------------------------------------
boss_data = np.loadtxt('pk_DR12CMASS_North_z0.57.txt', skiprows=1)
obs_k = boss_data[:,0]
obs_pk = boss_data[:,1]
obs_err_pk = boss_data[:,2]

print(f"✅ Loaded {len(obs_k)} synthetic BOSS P(k) points at z~0.57.")

# ----------------------------------------
# 3️⃣ Set up CAMB base parameters
# ----------------------------------------
base_pars = camb.CAMBparams()
base_pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122)
base_pars.set_matter_power(redshifts=[0.57], kmax=2.0)
base_pars.set_for_lmax(2500, lens_potential_accuracy=0)

# ----------------------------------------
# 4️⃣ Scan over ns values
# ----------------------------------------
ns_values = np.linspace(0.90, 0.98, 20)
chi2_tt_values, chi2_pk_values, chi2_total_values = [], [], []

for ns in ns_values:
    pars = base_pars.copy()
    pars.InitPower.set_params(As=2.1e-9, ns=ns, r=0.0, pivot_scalar=0.05)
    print(f"Running ns={ns:.3f}...")

    results = camb.get_results(pars)

    # ---- TT spectrum
    powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
    totCL = powers['total']
    ells = np.arange(totCL.shape[0])

    model_tt_interp = interp1d(ells, totCL[:,0], bounds_error=False, fill_value=np.nan)
    model_dl = model_tt_interp(obs_ell)

    valid_tt = np.isfinite(model_dl) & np.isfinite(obs_dl) & np.isfinite(obs_err)
    res_tt = (obs_dl[valid_tt] - model_dl[valid_tt]) / obs_err[valid_tt]
    chi2_tt = np.sum(res_tt**2)
    dof_tt = np.sum(valid_tt) - 1
    red_chi2_tt = chi2_tt / dof_tt

    # ---- Matter P(k)
    kh, z, pk = results.get_matter_power_spectrum(minkh=1e-4, maxkh=2.0, npoints=200)
    model_pk_interp = interp1d(kh, pk[0], bounds_error=False, fill_value=np.nan)
    model_pk = model_pk_interp(obs_k)

    valid_pk = np.isfinite(model_pk) & np.isfinite(obs_pk) & np.isfinite(obs_err_pk)
    res_pk = (obs_pk[valid_pk] - model_pk[valid_pk]) / obs_err_pk[valid_pk]
    chi2_pk = np.sum(res_pk**2)
    dof_pk = np.sum(valid_pk) - 1
    red_chi2_pk = chi2_pk / dof_pk

    chi2_total = chi2_tt + chi2_pk
    dof_total = dof_tt + dof_pk
    red_chi2_total = chi2_total / dof_total

    chi2_tt_values.append(red_chi2_tt)
    chi2_pk_values.append(red_chi2_pk)
    chi2_total_values.append(red_chi2_total)

    print(f"ns={ns:.3f}: χ²_TT={chi2_tt:.1f}, χ²_Pk={chi2_pk:.1f}, reduced χ²_total={red_chi2_total:.2f}")

# ----------------------------------------
# 5️⃣ Plotting
# ----------------------------------------
plt.figure(figsize=(8,6))
plt.plot(ns_values, chi2_total_values, 'o-', label=r'Reduced $\chi^2_\mathrm{total}$')
plt.plot(ns_values, chi2_tt_values, 's--', label=r'Reduced $\chi^2_\mathrm{TT}$')
plt.plot(ns_values, chi2_pk_values, 'd:', label=r'Reduced $\chi^2_{P(k)}$')
plt.xlabel(r'$n_s$')
plt.ylabel(r'Reduced $\chi^2$')
plt.title('Joint Fit of ns to Planck TT + BOSS P(k) Data')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('ns_joint_fit_chi2.png')
print("✅ Saved: ns_joint_fit_chi2.png")

# ----------------------------------------
# 6️⃣ Best-fit ns + 68% confidence interval
# ----------------------------------------
best_idx = np.argmin(chi2_total_values)
best_ns = ns_values[best_idx]
chi2_min = chi2_total_values[best_idx]
print(f"\n⭐ Best-fit ns={best_ns:.3f} with reduced χ²_total={chi2_min:.2f}")

delta_chi2_1sigma = 1.0
within_1sigma = np.array(chi2_total_values) <= (chi2_min + delta_chi2_1sigma)
if np.any(within_1sigma):
    ns_low = ns_values[within_1sigma][0]
    ns_high = ns_values[within_1sigma][-1]
    print(f"68% confidence interval on ns: {ns_low:.3f} – {ns_high:.3f}")
else:
    print("No ns range found within Δχ²=1 for 68% confidence interval.")

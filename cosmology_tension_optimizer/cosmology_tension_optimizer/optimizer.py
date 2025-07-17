import numpy as np
import subprocess

def main():
    print("Optimizer script is set up and running!")
    theta_init = np.array([70.0, 0.3, 0.96, 0.8, 0.0, -1e-5, 3.046, 0.0])
    print(f"Initial parameter vector: {theta_init}")
    
    write_config_files(theta_init)
    run_mcmc_pipeline()
    loss = compute_total_geodesic_loss(theta_init)
    print(f"Total dummy loss: {loss:.5f}")

def compute_total_geodesic_loss(theta):
    """
    Placeholder for computing total geodesic loss given parameter vector theta.
    """
    dummy_loss = np.sum(np.abs(theta))
    print(f"[DEBUG] Dummy loss computed: {dummy_loss:.5f}")
    return dummy_loss

def write_config_files(theta):
    """
    Write MGCAMB params.ini and Cobaya YAML config with current theta.
    """
    H0, Om, ns, sigma8, Omega_ede, fR0, Neff, f_decay = theta
    
    with open("params.ini", "w") as f:
        f.write(f"""use_mg = T
mg_model = fR
fR0 = {fR0}
H0 = {H0}
omega_lambda = {1-Om}
ns = {ns}
sigma8 = {sigma8}
""")
    
    with open("cobaya_fR.yaml", "w") as f:
        f.write(f"""likelihood:
  planck_2018_highl.TTTEEE: null
  sh0es: {{ H0: [{H0:.1f}, 1.3] }}
  des_y3: {{ type: 3x2pt }}

theory:
  mgcamb:
    path: ./MGCAMB
    model: fR
    extra_args:
      fR0: {fR0}
      n: 1
params:
  H0: {{prior: {{min: 60, max: 80}}, proposal: 0.5}}
  ombh2: {{prior: {{min: 0.019, max: 0.026}}, proposal: 0.0001}}
  omch2: {{prior: {{min: 0.1, max: 0.2}}, proposal: 0.001}}
  ns: {{prior: {{min: 0.9, max: 1.0}}, proposal: 0.002}}
  sigma8: {{prior: {{min: 0.7, max: 0.9}}, proposal: 0.01}}
  fR0: {{prior: {{min: -1e-4, max: 0}}, proposal: 1e-6}}
sampler:
  mcmc: {{Rminus1_stop: 0.01}}
output: chains/fR_test
""")
    print("[INFO] Configuration files written with current parameters.")

def run_mcmc_pipeline():
    """
    Run Cobaya with the current YAML configuration.
    """
    print("[INFO] Starting MCMC pipeline using Cobaya...")
    try:
        subprocess.run(["cobaya-run", "cobaya_fR.yaml"], check=True)
        print("[INFO] MCMC run completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] MCMC pipeline failed: {e}")

if __name__ == "__main__":
    main()

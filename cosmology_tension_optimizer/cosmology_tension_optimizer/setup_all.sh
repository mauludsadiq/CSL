#!/bin/bash
set -e

# 1) Create your custom likelihood Python file
cat > cosmology_tension_optimizer/my_likelihood.py <<EOF
from cobaya.likelihood import Likelihood
import numpy as np

class PkLikelihood(Likelihood):
    data_file = "cosmology_tension_optimizer/pk_DR12CMASS_North.txt"

    def initialize(self):
        data = np.loadtxt(self.data_file)
        self.k_data = data[:, 0]
        self.pk_data = data[:, 1]
        self.pk_error = data[:, 2]
        self.num_points = len(self.k_data)

    def get_requirements(self):
        return {"Pk": {"z": 0.57, "k_max": max(self.k_data)}}

    def logp(self, **params_values):
        pk_theory = self.provider.get_Pk(z=0.57, k=self.k_data)
        chi2 = np.sum(((self.pk_data - pk_theory) / self.pk_error) ** 2)
        return -0.5 * chi2
EOF

# 2) Write your P(k) data file
cat > cosmology_tension_optimizer/pk_DR12CMASS_North.txt <<EOF
1.000000e-02 3.630296e+05 3.630296e+04
1.211528e-02 2.340779e+05 2.340779e+04
1.467799e-02 1.994312e+05 1.994312e+04
1.778279e-02 1.206818e+05 1.206818e+04
2.154435e-02 1.024134e+05 1.024134e+04
2.610157e-02 7.615749e+04 7.615749e+03
3.162278e-02 5.793894e+04 5.793894e+03
3.831187e-02 4.472598e+04 4.472598e+03
4.641589e-02 2.948160e+04 2.948160e+03
5.623413e-02 2.565982e+04 2.565982e+03
6.812921e-02 1.650988e+04 1.650988e+03
8.254042e-02 1.295238e+04 1.295238e+03
1.000000e-01 1.104232e+04 1.104232e+03
1.211528e-01 7.138761e+03 7.138761e+02
1.467799e-01 5.458451e+03 5.458451e+02
1.778279e-01 4.567289e+03 4.567289e+02
2.154435e-01 3.060065e+03 3.060065e+02
2.610157e-01 2.574705e+03 2.574705e+02
3.162278e-01 1.703981e+03 1.703981e+02
3.831187e-01 1.178661e+03 1.178661e+02
4.641589e-01 1.058031e+03 1.058031e+02
5.623413e-01 7.377275e+02 7.377275e+01
6.812921e-01 4.313653e+02 4.313653e+01
8.254042e-01 4.092231e+02 4.092231e+01
1.000000e+00 3.413533e+02 3.413533e+01
EOF

# 3) Replace your cobaya_fr.yaml with the correct likelihood reference
cat > cobaya_fr.yaml <<EOF
theory:
  camb:
    path: ./MGCAMB
    extra_args:
      fR0: -1e-5
      n: 1

likelihood:
  PkLikelihood:
    module: cosmology_tension_optimizer.my_likelihood

params:
  H0: {prior: {min: 60, max: 80}, proposal: 0.5}
  ombh2: {prior: {min: 0.019, max: 0.026}, proposal: 0.0001}
  omch2: {prior: {min: 0.09, max: 0.15}, proposal: 0.001}
  ns: {prior: {min: 0.9, max: 1.0}, proposal: 0.002}
  sigma8: {prior: {min: 0.7, max: 0.9}, proposal: 0.01}
  fR0: {prior: {min: -1e-4, max: 0}, proposal: 1e-6}

sampler:
  mcmc: {Rminus1_stop: 0.01}

output: chains/fR_test
EOF

echo "✅ All files set up successfully!"

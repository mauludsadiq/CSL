from cobaya.likelihood import Likelihood
import numpy as np

class PkLikelihood(Likelihood):
    def initialize(self):
        self.data = np.loadtxt(self.data_file)
        self.k = self.data[:,0]
        self.Pk_obs = self.data[:,1]
        self.Pk_err = self.data[:,2]

    def logp(self, **params_values):
        Pk_model = self.theory.get_Pk_interpolator()(self.k)
        chi2 = np.sum(((self.Pk_obs - Pk_model) / self.Pk_err)**2)
        return -0.5 * chi2

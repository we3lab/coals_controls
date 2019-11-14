"""
Maximum Likelihood Estimator for censored observations.

This is an estimator based on the GenericLikelihoodModel class in statsmodels which takes into account that some
observations may be censored, as is often the case in environmental statistics.  Almost all of this code is based on
code by Github user  marianneke

Sources:
    - https://en.wikipedia.org/wiki/Maximum_likelihood_estimation
    - https://en.wikipedia.org/wiki/Censoring_(statistics)
    - https://github.com/marianneke/censored_likelihood
"""

import numpy as np
from scipy.stats import norm
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel


def _initial_values_params(target,x):
    """Use OLS regression to initialize paramters."""
    return sm.OLS(target,x).fit().params


def _ll_ols_obs(target, x, beta, sigma):
    """ Compute the log-likelihood for non-censored observations.

    :param list-like target: observed target variable
    :param matrix x:  features
    :param list-like beta: parameters
    :param float sigma: standard deviation
    :return: log-likelihood for non-censored variables
    """
    mu = x.dot(beta)
    return norm(mu, sigma).logpdf(target).sum()


def _ll_ols_cens(target, x, beta, sigma):
    """
    Compute the log-likelihood for non-censored observations.

    :param list-like target: observed target variables
    :param matrix x: features
    :param list-like beta: parameters
    :param float sigma: standard deviation
    :return: log-likelihood for censored variables
    """
    mu = x.dot(beta)
    return norm(mu, sigma).logcdf(target).sum()

def _ll_ols(y, x, beta, sigma):
    """ Compute log-likelihood with possibly censored data.

    :param matrix-like y:  matrix where the first column is the target variable and the second column is a boolean
        column indicating whether the target variable is observed (1) or left-censored (0)
    :param matrix x: features
    :param list-like beta: parameters
    :param float sigma:  standard deviation
    :return: log-likelihood
    """
    if y.shape[1] == 1:
        return _ll_ols_obs(y, x, beta, sigma)

    boolean_variables = y[:, 1]
    observed_values = y[:, 0]
    target_obs = []
    target_cens = []
    x_obs = []
    x_cens = []
    i = 0
    while i < len(boolean_variables):
        if boolean_variables[i] == 1:
            target_obs.append(observed_values[i])
            x_obs.append(x[i])
        elif boolean_variables[i] == 0:
            target_cens.append(observed_values[i])
            x_cens.append(x[i])
        i += 1

    target_obs = np.array(target_obs)
    target_cens = np.array(target_cens)
    x_obs = np.array(x_obs)
    x_cens = np.array(x_cens)

    if len(x_cens) != 0:
        ll_obs = _ll_ols_obs(target_obs, x_obs, beta, sigma)
        ll_cens = _ll_ols_cens(target_cens, x_cens, beta, sigma)

        return ll_obs + ll_cens
    else:
        ll_obs = _ll_ols_obs(target_obs, x_obs, beta, sigma)

        return ll_obs


class CensoredLikelihoodOLS(GenericLikelihoodModel):
    """Maximum likelihood estimation for censored data."""

    def __init__(self, endog, exog, **kwds):
        """
        Maximum likelihood estimation for left-censored data.

        This class defines a model for estimating OLS paramters using maximum likelihood estimation for target data that
        may be left-censored.  This is common in environmental data where concentrations may be below either reporting
        limits or detection limits.

        :param endog: contains the target variable in the first column, and a boolean column indicating whether the
            sample was observed (1) or is censored (0)
        :param exog:  any independent variables that are to be included in the model.  If an intercept is to be fitted,
            this should be added explicitly as a column containing ones for all observations
        """
        super(CensoredLikelihoodOLS, self).__init__(endog, exog, **kwds)

    def nloglikeobs(self, params):
        """ Compute the negative log likelihood to pass into the optimizer."""
        sigma = params[-1]
        beta = params[: -1]
        ll = _ll_ols(self.endog, self.exog, beta, sigma)
        return -ll

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
        """Fit OLS using maximum likelihood estimation."""
        # We have one additional parametmer and we need to add it for the summary.
        self.exog_names.append('sigma')
        if start_params is None:
            # Initialize starting values using the results of OLS regression
            start_params = np.append(_initial_values_params(self.endog[:,0], self.exog), 0.5)
        return super(CensoredLikelihoodOLS, self).fit(start_params=start_params, maxiter=maxiter, maxfun=maxfun, **kwds)

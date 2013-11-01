"""
Cart-pole balancing with iFDD+
"""

import sys, os
from Tools import Logger
from Domains import Pendulum_InvertedBalance
from Agents import Greedy_GQ, SARSA, Q_Learning
from Representations import *
from Policies import eGreedy
from Experiments import Experiment
import numpy as np
from hyperopt import hp

param_space = {'discretization': hp.quniform("discretization", 5, 40, 1),
               'boyan_N0': hp.loguniform("boyan_N0", np.log(1e1), np.log(1e5)),
               'initial_alpha': hp.loguniform("initial_alpha", np.log(1e-3), np.log(1))}


def make_experiment(id=1, path="./Results/Temp/{domain}/{agent}/{representation}/",
                    lambda_=0.,
                    boyan_N0=21.492871,
                    initial_alpha=0.0385705,
                    discretization=6.):
    logger = Logger()
    max_steps = 50000
    num_policy_checks = 20
    checks_per_policy = 10
    sparsify = True

    domain = Pendulum_InvertedBalance(logger=logger)

    representation = IndependentDiscretization(domain, logger, discretization=discretization)
    policy = eGreedy(representation, logger, epsilon=0.1)
    agent = Greedy_GQ(representation, policy, domain, logger,
                       lambda_=lambda_, 
                       BetaCoef=1e-6,
                       initial_alpha=initial_alpha,
                       alpha_decay_mode="boyan", boyan_N0=boyan_N0)
    experiment = Experiment(**locals())
    return experiment

if __name__ == '__main__':
    experiment = make_experiment(1)
    experiment.run()
    experiment.save()
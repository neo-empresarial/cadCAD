from ._utils import init_param_dist
import numpy as np
import numpy.random as npr 
from scipy.stats import expon

## Policies

def p_exposed_growth(params, substep, state_history, prev_state):
    N = prev_state['susceptible'] + prev_state['exposed'] + prev_state['infected'] + prev_state['recovered'] 
    S = prev_state['susceptible']
    I = prev_state['infected']

    r0 = init_param_dist(params['r0_dist'], params['rand_seed']).rvs(1)
    gamma = 1/(init_param_dist(params['gamma_dist'], params['rand_seed']).rvs(1))
    beta = r0*gamma

    SE = npr.binomial(S,
                      expon(scale=1/(beta*I/N)).cdf(1))

    return {'exposed_growth': np.ceil(SE[0])}


def p_infected_growth(params, substep, state_history, prev_state):
    E = prev_state['exposed']

    alpha = 1/(init_param_dist(params['alpha_dist'], params['rand_seed']).rvs(1))

    EI = npr.binomial(E,
                      expon(scale=1/alpha).cdf(1))[0]

    return {'infected_growth': np.ceil(EI)}


def p_recovered_growth(params, substep, state_history, prev_state):
    I = prev_state['infected']

    gamma = 1/(init_param_dist(params['gamma_dist'], params['rand_seed']).rvs(1))
    
    IR = npr.binomial(I,
                      expon(scale=1/gamma).cdf(1))[0]

    return {'recovered_growth': np.ceil(IR)}


## SUFs

def s_susceptible_population(params, substep, state_history, prev_state, policy_input):
    updated_susceptible_population = prev_state['susceptible'] - policy_input['exposed_growth']
    return ('susceptible', max(updated_susceptible_population, 0))


def s_exposed_population(params, substep, state_history, prev_state, policy_input):
    updated_exposed_population = prev_state['exposed'] + policy_input['exposed_growth'] - policy_input['infected_growth']
    return ('exposed', max(updated_exposed_population, 0))


def s_infected_population(params, substep, state_history, prev_state, policy_input):
    updated_infected_population = prev_state['infected'] + policy_input['infected_growth'] - policy_input['recovered_growth']
    return ('infected', max(updated_infected_population, 0))
        

def s_recovered_population(params, substep, state_history, prev_state, policy_input):
    updated_recovered_population = prev_state['recovered'] + policy_input['recovered_growth']
    return ('recovered', max(updated_recovered_population, 0))
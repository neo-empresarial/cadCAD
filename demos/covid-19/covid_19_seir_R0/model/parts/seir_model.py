import numpy as np 


## Policies

def p_exposed_growth(params, substep, state_history, prev_state):
    exposed_population = prev_state['reproductive_number']['value']*prev_state['infected']*(prev_state['susceptible']/(prev_state['susceptible']+ prev_state['exposed'] + prev_state['infected'] + prev_state['recovered']))
    return {'exposed_growth': np.ceil(exposed_population)}

def p_infected_growth(params, substep, state_history, prev_state):
    infected_population = params['exposure_rate']*prev_state['exposed']
    return {'infected_growth': np.ceil(infected_population)}

def p_recovered_growth(params, substep, state_history, prev_state):
    recovered_population = params['recovering_rate']*prev_state['infected']
    return {'recovered_growth': np.ceil(recovered_population)}

def p_incidence_growth(params, substep, state_history, prev_state):
    incidence_cases = params['exposure_rate']*prev_state['exposed']
    return {'incidence_growth': np.ceil(incidence_cases)}

def p_reproductive_number_mutation(params, substep, state_history, prev_state):
    total_infecteds = prev_state['recovered']+prev_state['infected']+prev_state['exposed']
    current_timestep = state_history[-1][0]['timestep']
    if(total_infecteds >= (2*prev_state['reproductive_number']['infected_amount'])): 
        doubling_time = current_timestep - prev_state['reproductive_number']['last_mutation']
        K = np.log(2)/doubling_time
        r0 = 1 + K*(params['exposure_time']+params['infected_time']) + (K**2)*(params['exposure_time']*params['infected_time'])

        reproductive_number = {
            'value': r0*params['recovering_rate'],
            'r0': r0, 
            'K': K, 
            'last_mutation': current_timestep, 
            'infected_amount': total_infecteds
        }
    else:
        reproductive_number = prev_state['reproductive_number']
    return {'reproductive_number_mutation': reproductive_number}


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

def s_incidence_population(params, substep, state_history, prev_state, policy_input):
    return ('incidence', max(policy_input['incidence_growth'], 0))


def s_reproductive_number(params, substep, state_history, prev_state, policy_input):
    return ('reproductive_number', policy_input['reproductive_number_mutation'])
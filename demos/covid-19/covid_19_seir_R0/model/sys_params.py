sys_params = {
        # 𝛽:  expected amount of people an infected person infects per day
        'infection_rate': [3],        
        # 𝛾: the proportion of infected recovering per day ( 𝛾  = 1/D)
        'recovering_rate': [1/4],
        # 𝛿: expected rate that exposed people turn into infected
        'exposure_rate': [1/3],
        # Te: average duration of the exposed state
        'exposure_time': [3.4],
        # Ti: average duration that a person infected can infect others
        'infected_time': [7.5]
}

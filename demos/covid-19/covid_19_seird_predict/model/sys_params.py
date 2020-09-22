sys_params = {
        # 𝛽:  expected amount of people an infected person infects per day
        'infection_rate': [0.035714, 0.057143, 0.078571, 0.1],        
        # 𝛾: the proportion of infected recovering per day ( 𝛾  = 1/D)
        'recovering_rate': [1/14],
        # 𝛿: expected rate that exposed people turn into infected
        'exposure_rate': [1/3],
        # α: death rate
        'death_rate': [0.01],
        # ρ: proportion of people dying daily, or (1/ρ) = days from infection until death
        'death_proportion_rate': [1/9] # 9 days from infection do death
}

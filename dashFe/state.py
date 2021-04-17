import pandas as pd

actions_assim = [0]
rewards_assim = [0]
randomactions_assim = [0]
randomrewards_assim = [0]
origactions_assim = [0]
actions_heat = [0]
rewards_heat = [0]
randomactions_heat = [0]
randomrewards_heat = [0]
origactions_heat = [0]
actions_water = [0]
rewards_water = [0]
randomactions_water = [0]
randomrewards_water = [0]
origactions_water = [0]
params = [
    "time",
    "AssimLight",
    "BlackScr",
    "CO2air",
    "Cum_irr",
    "EC_drain_PC",
    "EnScr",
    "HumDef",
    "PipeGrow",
    "PipeLow",
    "Rhair",
    "Tair",
    "Tot_PAR",
    "Tot_PAR_Lamps",
    "VentLee",
    "Ventwind",
    "co2_dos",
    "pH_drain_PC",
    "water_sup",
    "ProdA",
    "ProdB",
    "avg_nr_harvested_trusses",
    "Truss_development_time",
    "Nr_fruits_ClassA",
    "Weight_fruits_ClassA",
    "Nr_fruits_ClassB",
    "Weight_fruits_ClassB",
    "Flavour",
    "TSS",
    "Acid",
    "Juice",
    "Bite",
    "Weight",
    "DMC_fruit",
    "Stem_elong",
    "Stem_thick",
    "Cum_trusses",
    "stem_dens",
    "plant_dens",
]

obs = pd.DataFrame(columns=params)

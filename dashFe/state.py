import pandas as pd

c1 = ["light", "heat", "water"]
c2 = ["original", "predicted", "random"]
actions = {}
for c in c1:
    actions[c] = {}
    for cat in c2:
        actions[c][cat] = [0]

rewards = {}
for c in c1:
    rewards[c] = {}
    for cat in c2:
        if cat != "orginal":
            rewards[c][cat] = [0]

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

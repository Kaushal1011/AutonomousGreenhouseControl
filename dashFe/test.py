import requests
import json

actions_assim = []
rewards_assim = []
# call api to reset
r = requests.get("http://0.0.0.0:8000/light/reset")
if r.status_code != 200:
    raise Exception("status response is not 200")
obs = r.json()["data"][0]
# print(obs)
# call api to make predictions
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
payload = json.dumps({k: v for (k, v) in zip(params, obs)})
# print(payload)
r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
if r.status_code != 200:
    raise Exception("status response is not 200")
actions_assim.append(r.json()["data"][0])
# print("Action")
# print(actions_assim)
payload = json.dumps({"action": actions_assim[-1]})
r = requests.post("http://0.0.0.0:8000/light/environment", data=payload)
if r.status_code != 200:
    raise Exception("status response is not 200")
data = r.json()["data"][0]
obs = data["obs"]
reward = data["reward"]

print(obs)
print(reward)

rewards_assim.append(reward)
# call api to make predictions
payload = json.dumps({k: v for (k, v) in zip(params, obs)})
r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
if r.status_code != 200:
    raise Exception("status response is not 200")
actions_assim.append(r.json()["data"][0])
print(actions_assim)
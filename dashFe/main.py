import dash
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import requests

# some globals
actions_assim = []
rewards_assim = []
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

# obs = env_assim.resetinit()
# obs = list(obs)
# prediction = assim_model.predict([obs])
# action = np.argmax(prediction[0])
# actions_assim.append(action)


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.layout = html.Div(
    [
        # html.Button("Start Simulation", id="start", n_clicks=0),
        # html.Button("Stop Simulation", id="stop", n_clicks=0),
        html.Button("Reset Simulation", id="reset", n_clicks=0),
        dcc.Interval(
            id="interval-component", interval=100, n_intervals=0  # in milliseconds
        ),
        dcc.Graph(id="live-update-graph"),
    ]
)


# @app.callback(
#     dash.dependencies.Output("interval-component", "disable"),
#     [
#         dash.dependencies.Input("stop", "n_click"),
#         dash.dependencies.Input("start", "n_click"),
#     ],
# )
# def start_stop_live(start, stop):
#     ctx = dash.callback_context
#     btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     if btn_id == "start":
#         return True
#     return False


# def reset(n_clicks):
#     actions_assim = []
#     rewards_assim = []
#     # call api to reset
#     r = requests.get("http://0.0.0.0:8000/light/reset")
#     if r.status_code != 200:
#         raise Exception("status response is not 200")
#     obs = r.json()["data"][0]
#     # print(obs)
#     # call api to make predictions
#     payload = json.dumps({k: v for (k, v) in zip(params, obs)})
#     # print(payload)
#     r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
#     if r.status_code != 200:
#         raise Exception("status response is not 200")
#     actions_assim.append(r.json()["data"][0])


@app.callback(
    Output("live-update-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph(n):
    print("update graph")
    print(actions_assim)
    payload = json.dumps({"action": actions_assim[-1]})
    r = requests.post("http://0.0.0.0:8000/light/environment", data=payload)
    # if r.status_code != 200:
    #     raise Exception("status response is not 200")
    data = r.json()["data"][0]
    obs = data["obs"]
    reward = data["reward"]

    # print(obs)
    # print(reward)

    rewards_assim.append(reward)
    # call api to make predictions
    payload = json.dumps({k: v for (k, v) in zip(params, obs)})
    r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
    # if r.status_code != 200:
    #     raise Exception("status response is not 200")
    actions_assim.append(r.json()["data"][0])
    print(actions_assim)
    print(rewards_assim)
    fig = px.line(y=actions_assim)
    return fig


server = app.server
app.title = "AGC | RL"

if __name__ == "__main__":
    app.run_server(debug=True)
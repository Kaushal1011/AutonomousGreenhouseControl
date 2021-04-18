import dash
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import requests
import state
import json

# obs = env_assim.resetinit()
# obs = list(obs)
# prediction = assim_model.predict([obs])
# action = np.argmax(prediction[0])
# actions_assim.append(action)
API_URL = "http://0.0.0.0:8000"
env_type = ["Light", "Water", "Heat"]
available_team = [1, 2, 3, 4, 5]
sim_index = 0

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


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
        html.Button("Start Simulation", id="start", n_clicks=0),
        html.Button("Stop Simulation", id="stop", n_clicks=0),
        html.Button("Reset Simulation", id="reset", n_clicks=0),
        html.Div(
            [
                dcc.Dropdown(
                    id="demo-dropdown",
                    options=[
                        {"label": "Light", "value": "light"},
                        {"label": "Water", "value": "water"},
                        {"label": "Heat", "value": "heat"},
                    ],
                    value="light",
                )
            ]
        ),
        dcc.Interval(
            id="interval-component", interval=2000, n_intervals=0  # in milliseconds
        ),
        dcc.Graph(id="live-action-graph"),
        dcc.Graph(id="live-reward-graph"),
        dcc.Graph(id="live-obs-graph"),
    ]
)


@app.callback(
    dash.dependencies.Output("interval-component", "disabled"),
    [
        dash.dependencies.Input("stop", "n_clicks"),
        dash.dependencies.Input("start", "n_clicks"),
    ],
)
def start_stop_live(start, stop):
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"].split(".")[0] == "start":
        return False
    return True


def reset_graph():

    state.actions_assim = [0]
    state.rewards_assim = [0]
    state.randomactions_assim = [0]
    state.randomrewards_assim = [0]
    state.origactions_assim = [0]
    state.actions_heat = [0]
    state.rewards_heat = [0]
    state.randomactions_heat = [0]
    state.randomrewards_heat = [0]
    state.origactions_heat = [0]
    state.actions_water = [0]
    state.rewards_water = [0]
    state.randomactions_water = [0]
    state.randomrewards_water = [0]
    state.origactions_water = [0]
    # call api to reset
    r = requests.get(API_URL + "/light/reset")
    if r.status_code != 200:
        raise Exception("status response is not 200")
    obs = r.json()["data"][0]
    # print(obs)
    # call api to make predictions
    payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
    # print(payload)
    r = requests.post(API_URL + "/light/predict", data=payload)
    if r.status_code != 200:
        raise Exception("status response is not 200")
    state.actions_assim.append(r.json()["data"][0])
    fig = px.line(y=state.actions_assim)
    return fig


@app.callback(
    Output("live-action-graph", "figure"),
    Output("live-reward-graph", "figure"),
    Output("live-obs-graph", "figure"),
    [Input("interval-component", "n_intervals"), Input("reset", "n_clicks")],
)
def update_graph(reset, n):
    ctx = dash.callback_context
    # reset graph
    if ctx.triggered[0]["prop_id"].split(".")[0] == "reset":
        return reset_graph()

    for i in range(5):
        payload = json.dumps({"action": state.actions_assim[-1]})
        # print(payload)
        r = requests.post(API_URL + "/light/environment", data=payload)
        if r.status_code != 200:
            raise Exception("status response is not 200")
        data = r.json()["data"][0]
        obs = data["obs"]
        reward = data["reward"]
        obs_series = pd.Series(obs, index=state.params)
        state.obs = state.obs.append(obs_series, ignore_index=True)
        # print(state.obs)
        # print(reward)

        state.rewards_assim.append(reward + state.rewards_assim[-1])
        # call api to make predictions
        payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
        r = requests.post(API_URL + "/light/predict", data=payload)
        if r.status_code != 200:
            raise Exception("status response is not 200")
        state.actions_assim.append(r.json()["data"][0])

        r = requests.get(API_URL + "/light/randomstep")
        if r.status_code != 200:
            raise Exception("status response is not 200")
        data = r.json()["data"][0]
        state.randomactions_assim.append(data["randomaction"])
        state.randomrewards_assim.append(
            data["randomreward"] + state.randomrewards_assim[-1]
        )
        state.origactions_assim.append(data["action"])
        # call api to get random action random reward and orignal action

    # print(state.actions_assim)
    # print(state.rewards_assim)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=state.actions_assim, name="predicted actions"))
    fig1.add_trace(go.Scatter(y=state.randomactions_assim, name="random actions"))
    fig1.add_trace(go.Scatter(y=state.origactions_assim, name="orignal actions"))

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=state.rewards_assim, name="reward predicted actions"))
    fig2.add_trace(
        go.Scatter(y=state.randomrewards_assim, name="reward random actions")
    )

    data = [
        go.Scatter(y=state.obs[col], name=col) for col in state.params if col != "time"
    ]

    fig3 = go.Figure(data=data)
    return fig1, fig2, fig3


server = app.server
app.title = "AGC | RL"

if __name__ == "__main__":
    app.run_server(debug=True)

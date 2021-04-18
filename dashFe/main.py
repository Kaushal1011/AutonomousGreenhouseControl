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
        dbc.Row(
            [
                html.Button("Start Simulation", id="start", n_clicks=0),
                html.Button("Stop Simulation", id="stop", n_clicks=0),
                html.Button("Reset Simulation", id="reset", n_clicks=0),
                html.Button("Reset Team", id="reset-team", n_clicks=0),
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown",
                        options=[
                            {"label": "Light", "value": "light"},
                            {"label": "Water", "value": "water"},
                            {"label": "Heat", "value": "heat"},
                        ],
                        value="light",
                    ),
                    width={"size": 1},
                ),
                dcc.Input(
                    id="index",
                    type="number",
                    placeholder="Index",
                    min=0,
                    step=1,
                    debounce=True,
                ),
                dcc.Input(
                    id="team",
                    type="number",
                    placeholder="Team",
                    min=1,
                    max=5,
                    step=1,
                    debounce=True,
                ),
            ]
        ),
        dcc.Interval(
            id="interval-component", interval=2000, n_intervals=0  # in milliseconds
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="live-action-graph"), width={"size": 6}),
                dbc.Col(dcc.Graph(id="live-reward-graph"), width={"size": 6}),
            ]
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="live-obs-graph"), width={"size": 10, "offset": 1}),
            style={"height": "50vh"},
        ),
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


def reset_graph(cat, reset_team=False):
    state.actions = {}
    for c in state.c1:
        state.actions[c] = {}
        for category in state.c2:
            state.actions[c][category] = [0]

    state.rewards = {}
    for c in state.c1:
        state.rewards[c] = {}
        for category in state.c2:
            if category != "orginal":
                state.rewards[c][category] = [0]

    state.obs = pd.DataFrame(columns=state.params)
    # call api to reset
    if reset_team:
        r = requests.get(API_URL + "/{}/reset_team".format(cat))
        if r.status_code != 200:
            raise Exception("status response is not 200")
        obs = r.json()["data"][0]
    else:
        r = requests.get(API_URL + "/{}/reset".format(cat))
        if r.status_code != 200:
            raise Exception("status response is not 200")
        obs = r.json()["data"][0]
    # print(obs)
    # call api to make predictions
    payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
    # print(payload)
    r = requests.post(API_URL + "/{}/predict".format(cat), data=payload)
    if r.status_code != 200:
        raise Exception("status response is not 200")
    state.actions[cat]["predicted"].append(r.json()["data"][0])

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(y=state.actions[cat]["predicted"], name="predicted actions")
    )
    fig1.add_trace(go.Scatter(y=state.actions[cat]["random"], name="random actions"))
    fig1.add_trace(go.Scatter(y=state.actions[cat]["original"], name="orignal actions"))

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(y=state.rewards[cat]["predicted"], name="reward predicted actions")
    )
    fig2.add_trace(
        go.Scatter(y=state.rewards[cat]["random"], name="reward random actions")
    )

    data = [
        go.Scatter(y=state.obs[col], name=col) for col in state.params if col != "time"
    ]

    fig3 = go.Figure(data=data)
    return fig1, fig2, fig3


@app.callback(
    Output("live-action-graph", "figure"),
    Output("live-reward-graph", "figure"),
    Output("live-obs-graph", "figure"),
    [
        Input("interval-component", "n_intervals"),
        Input("reset", "n_clicks"),
        Input("reset-team", "n_clicks"),
        Input("index", "value"),
        Input("team", "value"),
        Input("dropdown", "value"),
    ],
)
def update_graph(n, reset, reset_team, index, team, cat):
    ctx = dash.callback_context
    # reset graph
    if ctx.triggered[0]["prop_id"].split(".")[0] == "reset":
        return reset_graph(cat)
    if ctx.triggered[0]["prop_id"].split(".")[0] == "dropdown":
        return reset_graph(cat)
    if ctx.triggered[0]["prop_id"].split(".")[0] == "reset-team":
        return reset_graph(cat, reset_team=True)

    if (
        ctx.triggered[0]["prop_id"].split(".")[0] == "index"
        or ctx.triggered[0]["prop_id"].split(".")[0] == "team"
    ):
        if not team:
            team = 0
        if not index:
            index = 0
        payload = json.dumps({"team": team, "index": index})
        requests.post(API_URL + "/{}/teamnindex".format(cat), data=payload)
        return reset_graph(cat)

    for i in range(5):
        payload = json.dumps({"action": state.actions[cat]["predicted"][-1]})
        # print(payload)
        r = requests.post(API_URL + "/{}/environment".format(cat), data=payload)
        if r.status_code != 200:
            raise Exception("status response is not 200")
        data = r.json()["data"][0]
        obs = data["obs"]
        reward = data["reward"]
        obs_series = pd.Series(obs, index=state.params)
        state.obs = state.obs.append(obs_series, ignore_index=True)
        # print(state.obs)
        # print(reward)

        state.rewards[cat]["predicted"].append(
            reward + state.rewards[cat]["predicted"][-1]
        )
        # call api to make predictions
        payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
        r = requests.post(API_URL + "/{}/predict".format(cat), data=payload)
        if r.status_code != 200:
            raise Exception("status response is not 200")
        state.actions[cat]["predicted"].append(r.json()["data"][0])

        r = requests.get(API_URL + "/{}/randomstep".format(cat))
        if r.status_code != 200:
            raise Exception("status response is not 200")
        data = r.json()["data"][0]
        state.actions[cat]["random"].append(data["randomaction"])
        state.rewards[cat]["random"].append(
            data["randomreward"] + state.rewards[cat]["random"][-1]
        )
        state.actions[cat]["original"].append(data["action"])
        # call api to get random action random reward and orignal action

    # print(state.actions[cat])
    # print(state.rewards_assim)
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(y=state.actions[cat]["predicted"], name="predicted actions")
    )
    fig1.add_trace(go.Scatter(y=state.actions[cat]["random"], name="random actions"))
    fig1.add_trace(go.Scatter(y=state.actions[cat]["original"], name="orignal actions"))

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(y=state.rewards[cat]["predicted"], name="reward predicted actions")
    )
    fig2.add_trace(
        go.Scatter(y=state.rewards[cat]["random"], name="reward random actions")
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

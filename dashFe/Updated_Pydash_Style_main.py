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
import state
import json


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/index")),
            dbc.DropdownMenu(
                children=[

                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Wine Dash",
        color="primary",
        dark=True,
    )
    return navbar


# obs = env_assim.resetinit()
# obs = list(obs)
# prediction = assim_model.predict([obs])
# action = np.argmax(prediction[0])
# actions_assim.append(action)
Action = ['Light', 'Water', 'Hit']
available_Team = [1, 2, 3, 4, 5]
available_sim = [1, 2, 3, 4, 5]

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

colors = {
    'background': '#6c757d',
    'text': '#fff'
}

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.layout = html.Div(style={'backgroundColor': colors ['background']}, children=[

    html.H1(
            children='AGC_RL_DASHBOARD',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

    html.Button("Start Simulation", id="start", n_clicks=0, style={
        'textAlign': 'center',
        'color': colors['text'],
        'height': 40,
        'padding': 40,
        'width': 250,
    }),
    html.Button("Stop Simulation", id="stop", n_clicks=0, style={
        'textAlign': 'center',
        'color': colors['text'],
        'height': 40,
        'padding': 40,
        'width': 250,
    }),
    html.Button("Reset Simulation", id="reset", n_clicks=0, style={
        'textAlign': 'center',
        'color': colors['text'],
        'height': 40,
        'padding': 40,
        'width': 250,
    }),
    html.Button("Set", id="set", n_clicks=0, style={
        'textAlign': 'center',
        'color': colors['text'],
        'height': 40,
        'padding': 40,
        'width': 250,
    }),
    dcc.Interval(
        id="interval-component", interval=1000, n_intervals=0  # in milliseconds
    ),

    dcc.Dropdown(
        id='Action-index',
        options=[{'label': i, 'value': i} for i in Action],
        placeholder="Action",
        style={
            'textAlign': 'center',
            'color': '#000',
            'height': 40,
            'width': 300,
            'backgroundColor': colors ['background']
        }

    ),

    dcc.Dropdown(
        id='Team-index',
        options=[{'label': i, 'value': i} for i in available_Team],
        placeholder="Team",
        style={
            'textAlign': 'center',
            'color': '#000',
            'height': 40,
            'width': 300,
            'backgroundColor': colors ['background']
        }

    ),
    dcc.Dropdown(
        id='sim-index',
        options=[{'label': i, 'value': i} for i in available_sim],
        placeholder="sim",
        style={
            'textAlign': 'center',
            'color': '#000',
            'height': 40,
            'width': 300,
            'backgroundColor': colors ['background']
        }

    ),
    dcc.Graph(id="live-update-graph"),
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
    if ctx.triggered [0] ["prop_id"].split(".") [0] == "start":
        return False
    return True


def reset_graph():
    state.actions_assim = [0]
    state.rewards_assim = []
    # call api to reset
    r = requests.get("http://0.0.0.0:8000/light/reset")
    if r.status_code != 200:
        raise Exception("status response is not 200")
    obs = r.json() ["data"] [0]
    # print(obs)
    # call api to make predictions
    payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
    # print(payload)
    r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
    if r.status_code != 200:
        raise Exception("status response is not 200")
    state.actions_assim.append(r.json() ["data"] [0])
    fig = px.line(y=state.actions_assim)
    return fig


@app.callback(
    Output("live-update-graph", "figure"),
    [Input("interval-component", "n_intervals"), Input("reset", "n_clicks")],
)
def update_graph(reset, n):
    ctx = dash.callback_context
    if ctx.triggered [0] ["prop_id"].split(".") [0] == "reset":
        return reset_graph()

    state.actions_assim.append(n)
    payload = json.dumps({"action": state.actions_assim [-1]})
    # print(payload)
    r = requests.post("http://0.0.0.0:8000/light/environment", data=payload)
    if r.status_code != 200:
        raise Exception("status response is not 200")
    data = r.json() ["data"] [0]
    obs = data ["obs"]
    reward = data ["reward"]

    # print(obs)
    # print(reward)

    state.rewards_assim.append(reward)
    # call api to make predictions
    payload = json.dumps({k: v for (k, v) in zip(state.params, obs)})
    r = requests.post("http://0.0.0.0:8000/light/predict", data=payload)
    if r.status_code != 200:
        raise Exception("status response is not 200")
    state.actions_assim.append(r.json() ["data"] [0])
    # print(state.actions_assim)
    # print(state.rewards_assim)
    fig = px.line(y=state.actions_assim)
    return fig


server = app.server
app.title = "AGC | RL"

if __name__ == "__main__":
    app.run_server(debug=True)

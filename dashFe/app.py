import QPSK
import QFSK
import MPSK
import Coding
import channel
import BPSK
import BFSK
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash
from typing import List, Tuple

#!/usr/bin/env python3

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]
colors = {"background": "#0e0e0e", "text": "#4ecca3", "options": "#fc7e2f"}

palatte = {
    "A": "#101010",
    "B": "#33415c",
    "C": "#5c677d",
    "D": "#7d8597",
    "E": "#f4f4f4",
    "F": "#2f2f2f",
}

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

server = app.server
app.title = "Dayummunication - BFSK QFSK BPSK QPSK"

t_csd = np.linspace(0.0, 2.0 * np.math.pi, 100)

# Default parameters
f_c = 100.0
t_c = 1.0 / f_c

# Sampling rate
f_s = 10000.0
t_s = 1.0 / f_s

# MPSK Parameters
Tb = 0.01
Eb = 0.001

fs_min = 10000
fs_max = 20000

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        dbc.Container(
            [
                html.H1(
                    children="Dayummunication",
                    style={
                        "textAlign": "center",
                        "mt": 10,
                        "mb": 10,
                        "color": colors["text"],
                    },
                ),
                html.H5(
                    children="Making digital communication look dayumm!",
                    style={
                        "textAlign": "center",
                        "mt": 10,
                        "mb": 10,
                        "color": colors["text"],
                    },
                ),
                html.Hr(),
                html.Div(
                    id="modulation-type",
                    children=[
                        html.H2(
                            children="Modulation Scheme",
                            style={
                                "mt": 10,
                                "mb": 10,
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        dcc.Dropdown(
                            id="modulation-scheme",
                            options=[
                                {
                                    "label": "Binary Phase Shift Keying (BPSK)",
                                    "value": "BPSK",
                                },
                                {
                                    "label": "Binary Frequency Shift Keying (BFSK)",
                                    "value": "BFSK",
                                },
                                {
                                    "label": "Quadrature Phase Shift Keying (QPSK)",
                                    "value": "QPSK",
                                },
                                {
                                    "label": "Quadrature Frequency Shift Keying (QFSK)",
                                    "value": "QFSK",
                                },
                                # {
                                #     "label": "M'ary Phase Shift Keying (MPSK)",
                                #     "value": "MPSK",
                                # },
                            ],
                            placeholder="For eg. BPSK",
                            value="BPSK",
                            style={"mt": 10, "mb": 10, "color": "white"},
                        ),
                    ],
                ),
            ],
            fluid=True,
        ),
        dbc.Container(
            id="modulation-params",
            children=[
                html.H4("Modulation Parameters"),
                html.H6(
                    "Please enter reasonable values for the parameters. If you're not sure, let them be."
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.Label(
                                    "Bit Energy - Eb (J)",
                                    style={"color": colors["options"]},
                                ),
                                dcc.Input(
                                    id="energy",
                                    value=0.001,
                                    type="number",
                                    style={"color": "white"},
                                    min=0.001,
                                    max=10,
                                ),
                            ],
                            sm=6,
                            md=4,
                            lg=3,
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Bit Time - Tb (s)",
                                    style={"color": colors["options"]},
                                ),
                                dcc.Input(
                                    id="bit-time",
                                    value=0.01,
                                    type="number",
                                    style={"color": "white"},
                                    min=0.001,
                                    max=5,
                                ),
                            ],
                            sm=6,
                            md=4,
                            lg=3,
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Carrier Frequency - fc (Hz)",
                                    style={"color": colors["options"]},
                                ),
                                dcc.Input(
                                    id="carrier-frequency",
                                    value=100,
                                    type="number",
                                    style={"color": "white"},
                                    min=100,
                                    max=fs_min / 8,
                                ),
                            ],
                            sm=6,
                            md=4,
                            lg=3,
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Sampling Frequency - fs (Hz)",
                                    style={"color": colors["options"]},
                                ),
                                dcc.Input(
                                    id="sampling-frequency",
                                    value=10000,
                                    type="number",
                                    style={"color": "white"},
                                    min=fs_min,
                                    max=fs_max,
                                ),
                            ],
                            sm=6,
                            md=4,
                            lg=3,
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Noise Power Spectral Density - N0 (W-Hz)",
                                    style={"color": colors["options"]},
                                ),
                                dcc.Input(
                                    id="noise-energy",
                                    value=0.000004,
                                    type="number",
                                    style={"color": "white"},
                                    min=0.00000000000000000001,
                                    max=10,
                                ),
                            ],
                            sm=6,
                            md=4,
                            lg=3,
                        ),
                    ]
                ),
                # dbc.Row(
                #     children=[
                #     ],
                # ),
            ],
            fluid=True
            # style={"columnCount": 3},
        ),
        dbc.Container(
            [
                html.Div(
                    # id="input",
                    # className="align-middle",
                    children=[
                        html.H2(
                            children="Input Signal",
                            style={
                                "mt": 10,
                                "mb": 10,
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        dcc.Textarea(
                            id="input-str",
                            value="0",
                            # type="text",
                            style={"mt": 10, "mb": 10, "color": "white"},
                        ),
                        html.Button(
                            id="submit-button-state",
                            n_clicks=0,
                            children="Submit",
                            style={"mt": 10, "mb": 10, "color": "white", "pb": 5},
                        ),
                        dcc.Checklist(
                            id="coding-flag",
                            options=[
                                {
                                    "label": "Encode. Encoding is done using extended Golay code i.e. [24, 12, 8] linear ECC.",
                                    "value": "True",
                                },
                            ],
                            labelStyle={"font-size": 16},
                            style={"margin": 5},
                        ),
                    ],
                ),
                html.Hr(),
                html.Div(id="container"),
                html.Div(
                    dcc.Graph(id="empty", figure={"data": []}),
                    style={"display": "none"},
                ),
                html.Hr(),
                html.H2("Bit Error Rate"),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H3(
                                    children="Theoretical",
                                    style={
                                        "mt": 10,
                                        "mb": 10,
                                        "textAlign": "center",
                                        "color": colors["text"],
                                    },
                                ),
                                html.H3(
                                    children="0",
                                    id="ber-theoretical",
                                    style={
                                        "mt": 10,
                                        "mb": 10,
                                        "textAlign": "center",
                                        "color": colors["text"],
                                    },
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            children=[
                                html.H3(
                                    children="Practical",
                                    style={
                                        "mt": 10,
                                        "mb": 10,
                                        "textAlign": "center",
                                        "color": colors["options"],
                                    },
                                ),
                                html.H3(
                                    children="0",
                                    id="ber-practical",
                                    style={
                                        "mt": 10,
                                        "mb": 10,
                                        "textAlign": "center",
                                        "color": colors["options"],
                                    },
                                ),
                            ],
                            md=6,
                        ),
                    ]
                ),
                html.Div(
                    # id="input",
                    # className="align-middle",
                    children=[
                        html.H2(
                            children="Output Signal",
                            style={
                                "mt": 10,
                                "mb": 10,
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        dcc.Textarea(
                            id="output-str",
                            # type="text",
                            style={"mt": 10, "mb": 10, "color": "white"},
                        ),
                    ]
                ),
                # dcc.Graph(id="signal",),
                # dcc.Graph(id="modulated-signal"),
                # dbc.Row(children=[
                # dbc.Col(dcc.Graph(id="noise"), md=12, lg=6),
                # dbc.Col(dcc.Graph(id="noise-signal"),
                # md=12, lg=6),
                # ]),
                # dcc.Graph(id="demodulated-signal"),
            ],
            fluid=True,
        ),
    ],
)


@app.callback(
    [
        # Output("signal", "figure"),
        # Output("modulated-signal", "figure"),
        # Output("noise", "figure"),
        # Output("noise-signal", "figure"),
        # Output("demodulated-signal", "figure"),
        Output("container", "children"),
        Output("ber-theoretical", "children"),
        Output("ber-practical", "children"),
        Output("output-str", "value"),
    ],
    [
        Input("submit-button-state", "n_clicks"),
        Input("coding-flag", "value"),
        Input("modulation-scheme", "value"),
        Input("energy", "value"),
        Input("bit-time", "value"),
        Input("carrier-frequency", "value"),
        Input("sampling-frequency", "value"),
        Input("noise-energy", "value"),
    ],
    [State("input-str", "value")],
)
def conv(
    n_clicks: int,
    coding_flag: str,
    modulation_scheme: str,
    Eb: int,
    Tb: int,
    f_c: int,
    f_s: int,
    N0: str,
    input_str: str,
) -> tuple:
    if n_clicks >= 0:

        chars = []
        for i in input_str:
            b = bin(ord(i))[2:]
            b = "0" + b if len(b) == 7 else "00" + b
            chars.append(b)

        chars = [int(i) for i in list("".join(chars))]
        charorig = None
        modulated_signal = None
        noise_signal = None
        signal_plus_noise = None
        demodulated_signal = None
        t = None
        ber_theoretical = 0
        ber_practical = 0
        out = None
        graphs = []

        binary_signal_figure = go.Figure()
        binary_signal_figure.add_trace(
            go.Scatter(
                x=list(range(len(chars))),
                y=chars,
                mode="lines+markers",
                marker=dict(color="#4ecca3"),
            )
        )
        binary_signal_figure.update_layout(
            title="Binary Signal",
            xaxis_title="Bit #",
            yaxis_title="Value",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )
        graphs.append(dcc.Graph(id="signal", figure=binary_signal_figure))

        try:
            if coding_flag[0] == "True":
                charsorig = chars
                chars = Coding.encodebits(chars)
                encoded_binary_signal_figure = go.Figure()
                encoded_binary_signal_figure.add_trace(
                    go.Scatter(
                        x=list(range(len(chars))),
                        y=chars,
                        mode="lines+markers",
                        marker=dict(color="#4ecca3"),
                    )
                )
                encoded_binary_signal_figure.update_layout(
                    title="Encoded Binary Signal",
                    xaxis_title="Bit #",
                    yaxis_title="Value",
                    paper_bgcolor=palatte["A"],
                    font=dict(color=palatte["E"], size=14),
                    template="plotly_dark",
                )
                graphs.append(
                    dcc.Graph(id="encoded-signal", figure=encoded_binary_signal_figure)
                )
        except (TypeError, IndexError):
            pass

        if modulation_scheme == "BPSK":
            modulated_signal = BPSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = BPSK.demodulate(signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))
            ber_theoretical, ber_practical = BPSK.error_probabilities(
                chars, demodulated_signal, Eb, N0
            )

        if modulation_scheme == "BFSK":
            modulated_signal = BFSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = BFSK.demodulate(signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))
            ber_theoretical, ber_practical = BFSK.error_probabilities(
                chars, demodulated_signal, Eb, N0
            )

        if modulation_scheme == "QPSK":
            modulated_signal = QPSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = QPSK.demodulate(signal_plus_noise, Tb, f_c, f_s)
            symbols = np.array([chars[0::2], chars[1::2]])
            t = np.linspace(
                0,
                np.size(symbols, axis=1) * Tb,
                int(np.size(symbols, axis=1) * Tb * f_s),
            )
            ser, ber_theoretical, ber_practical = MPSK.error_probabilities(
                chars, demodulated_signal, Eb, N0, 2, 4
            )

        if modulation_scheme == "QFSK":
            modulated_signal = QFSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = QFSK.demodulate(signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))
            ser, ber_theoretical, ber_practical = QFSK.error_probabilities(
                chars, demodulated_signal, Eb, N0
            )

        modulated_signal_figure = go.Figure()
        modulated_signal_figure.add_trace(
            go.Scatter(x=t, y=modulated_signal, marker=dict(color="#fc7e2f")),
        )
        modulated_signal_figure.update_layout(
            title="Modulated Signal",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )
        graphs.append(dcc.Graph(id="modulated-signal", figure=modulated_signal_figure))

        noise_figure = go.Figure()
        noise_figure.add_trace(
            go.Scatter(x=t, y=noise_signal, marker=dict(color="#4ecca3")),
        )
        noise_figure.update_layout(
            title="Additive White Gaussian Noise",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        noise_signal_figure = go.Figure()
        noise_signal_figure.add_trace(
            go.Scatter(x=t, y=signal_plus_noise, marker=dict(color="#fc7e2f")),
        )

        # noise_signal_figure = make_subplots(rows=1, cols=2)
        # noise_signal_figure.add_trace(
        #     go.Scatter(x=t, y=noise_signal, marker=dict(color="#4ecca3")), row=1, col=1,
        # )
        # noise_signal_figure.add_trace(
        #     go.Scatter(x=t, y=signal_plus_noise, marker=dict(color="#fc7e2f")), row=1, col=2,
        # )
        noise_signal_figure.update_layout(
            title="Modulation Signal + Noise Signal",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )
        graphs.append(
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(id="noise", figure=noise_figure), md=12, lg=6),
                    dbc.Col(
                        dcc.Graph(id="noise-signal", figure=noise_signal_figure),
                        md=12,
                        lg=6,
                    ),
                ]
            ),
        )

        demodulated_signal_figure = go.Figure()
        demodulated_signal_figure.add_trace(
            go.Scatter(
                x=t,
                y=demodulated_signal,
                mode="lines+markers",
                marker=dict(color="#4ecca3"),
            ),
        )
        demodulated_signal_figure.update_layout(
            title="Demodulated Signal",
            xaxis_title="Time (s)",
            yaxis_title="Value",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )
        graphs.append(
            dcc.Graph(id="demodulated-signal", figure=demodulated_signal_figure)
        )

        out = decode_to_str(demodulated_signal)

        try:
            if coding_flag[0] == "True":

                # Generate new plot for decoded signal
                decoded_signal = Coding.decodebits(demodulated_signal)
                decoded_signal_figure = go.Figure()
                decoded_signal_figure.add_trace(
                    go.Scatter(
                        x=t,
                        y=decoded_signal,
                        mode="lines+markers",
                        marker=dict(color="#4ecca3"),
                    ),
                )
                decoded_signal_figure.update_layout(
                    title="Decoded Signal",
                    xaxis_title="Time (s)",
                    yaxis_title="Value",
                    paper_bgcolor=palatte["A"],
                    font=dict(color=palatte["E"], size=14),
                    template="plotly_dark",
                )
                graphs.append(
                    dcc.Graph(id="decoded-signal", figure=decoded_signal_figure)
                )
                out = decode_to_str(decoded_signal)
                # Calculate new error_probabilities
                ber_theoretical_old = ber_theoretical
                ber_theoretical, ber_practical = Coding.error_probabilities(
                    charsorig, decoded_signal, Eb, N0, ber_theoretical_old
                )

                # Convert to string

        except (TypeError, IndexError):
            pass
        # return (
        #     binary_signal_figure,
        #     modulated_signal_figure,
        #     noise_figure,
        #     noise_signal_figure,
        #     demodulated_signal_figure,
        # )
        return (html.Div(graphs), ber_theoretical, ber_practical, out)


def decode_to_str(demodulated_signal: List[int]) -> str:
    chars: List[List[int]] = [
        demodulated_signal[i * 8 : (i + 1) * 8]
        for i in range(len(demodulated_signal) // 8)
    ]

    return "".join([chr(int("".join([str(j) for j in i]), base=2)) for i in chars])


if __name__ == "__main__":
    app.run_server(debug=True)

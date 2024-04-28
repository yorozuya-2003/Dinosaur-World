import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from app import app
import world

scroll_down_button = html.Div(
    children=[
        html.A(
            html.Button("▼", id="scroll-down-button"),
            href="#locate-dino"
        )
    ],
    id="scroll-down-container"
)

scroll_up_button = html.Div(
    children=[
        html.A(
            html.Button("▲", id="scroll-up-button"),
            href="#dino-world-home"
        )
    ],
    id="scroll-up-container"
)

layout = html.Div([
    html.Div(
        children=[
            html.Div(
                children=[scroll_down_button],
                id='dino-world-home',
                style={
                    'background-image': 'url("/assets/background.png")',
                    'background-size': 'cover', 
                    'background-repeat': 'no-repeat',
                    'background-position': 'center', 
                    'height': '100vh'
                }
            )
        ]
    ),
    # Main content below the header
    html.Div([world.layout], id='locate-dino'),
])
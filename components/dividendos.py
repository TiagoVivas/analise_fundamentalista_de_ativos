from dash import html, dcc
import dash_bootstrap_components as dbc

from app import app

# ============ Layout ============ #
layout = dbc.Col([
    dbc.Card([
        dcc.Graph(id='dividendos-grafico')
    ], style={'height': '100%', 'padding': '10px'})
])

# ============ Callbacks ============ #
from dash import html
import dash_bootstrap_components as dbc

from app import app

# ============ Layout ============ #
layout = dbc.Col([
# Seção Indicadores de Valuation ----------------
    html.Legend("Indicadores de Valuation"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H6("P/L",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-p/l',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("P/VP",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-p/vp',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("LPA",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-lpa',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2)
    ]),
    html.Hr(),

# Seção Indicadores de Endividamento ------------
    html.Legend("Indicadores de Endividamento"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H6("Div.Liq/PL",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-div.liq/pl',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("PL/Ativos",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-pl/ativos',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Passivos/Ativos",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-passivos/ativos',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Liquidez corrente",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-liquidez-corrente',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
    ]),
    html.Hr(),

# Seção Indicadores de Eficiência ---------------
    html.Legend("Indicadores de Eficiência"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H6("Margem Bruta",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-margem-bruta',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Margem líquida",
                        style={'textAlign': 'center'}),
                html.Label("X...%",
                            id='indicadores-margem-liquida',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2)
    ]),
    html.Hr()
])

# ============ Callbacks ============ #

"""
Indicadores de Valuation
P/L
P/VP
LPA

Indicadores de Endividamento
Div.Liq/PL
PL/Ativos
Passivos/Ativos
Liquidez corrente

Indicadores de Eficiência
Margem bruta
Margem líquida
"""
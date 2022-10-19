from dash import html, dcc
import dash_bootstrap_components as dbc

from datetime import datetime, timedelta

from app import app

# ============ Layout ============ #
layout = dbc.Col([
    dbc.Row([
# Seção filtros -------------------------
        dbc.Col([
            dbc.Card([
                html.Legend("Filtros de cotação"),
                html.Label("Período:",
                        style={'font-size': 18}),
                html.Div(dcc.Dropdown(id='cotacao-periodo',
                                      clearable=False,
                                      style={'width': '100%'},
                                      persistence=True,
                                      persistence_type='session',
                                      multi=False)),
                html.Label("Intervalo:",
                        style={'font-size': 18}),
                html.Div(dcc.Dropdown(id='cotacao-intervalo',
                                      clearable=False,
                                      style={'width': '100%'},
                                      persistence=True,
                                      persistence_type='session',
                                      multi=False)),
                html.Label("Período de análise", 
                        style={'font-size': 18}),
                dcc.DatePickerRange(id='cotacao-datas',
                                    month_format='D MMM, YY',
                                    end_date_placeholder_text='Data...',
                                    start_date=datetime.today() - timedelta(days=31),
                                    end_date=datetime.today(),
                                    updatemode='singledate',
                                    display_format='D/M/yyyy',
                                    style={'z-index': '100'})
            ], style={'height': '100%', 'padding': '10px'})
        ], width=3),
# Seção gráfico -------------------------
        dbc.Col([
            dbc.Card([
                    dcc.Graph(id='cotacao-grafico')
                ], style={'height': '100%', 'padding': '10px'})
        ], width=9)
    ])
])

# ============ Callbacks ============ #
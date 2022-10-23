from dash import html, dcc
import dash_bootstrap_components as dbc

from app import app

# ============ Layout ============ #
layout = dbc.Col([
# Seção de expectativas de preço ----------------------
    html.Legend("Expectativas de preço"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Label("Atual: R$ ...",
                           id='expectativas-preco-atual',
                           style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
                html.Label("Mediana: R$ ...",
                           id='expectativas-preco-mediana',
                           style={'font-size': 24, 'width': '100%', 'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Mín:",
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'}),
                        html.Label("R$ ...",
                                   id='expectativas-preco-min',
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'})
                    ]),
                    dbc.Col([
                        html.Label("Média:",
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'}),
                        html.Label("R$ ...",
                                   id='expectativas-preco-media',
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'})
                    ]), 
                    dbc.Col([
                        html.Label("Máx:",
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'}),
                        html.Label("R$ ...",
                                   id='expectativas-preco-max',
                                   style={'font-size': 14, 'width': '100%', 'textAlign': 'center'})
                    ])
                ])
            ])
        ], width=4),
        dbc.Col([
            dcc.Graph(id='expectativas-grafico')
        ], width=8)
    ]),
    html.Hr(),

# Seção Histórico de recomendações --------------------
    html.Legend("Histórico de recomendações"),
    html.H6("Há 1 mês:"),
    dcc.Graph(id='recomendacoes-grafico-1'),
    html.H6("Há 2 meses:"),
    dcc.Graph(id='recomendacoes-grafico-2'),
    html.H6("Há 3 meses:"),
    dcc.Graph(id='recomendacoes-grafico-3')
])

# ============ Callbacks ============ #

"""
Preço atual > yq.financial_data.currentPrice
Expectativa mínima > yq.financial_data.targetLowPrice
Expectativa máxima > yq.financial_data.targetHighPrice
Expectativa média > yq.financial_data.targetMeanPrice
Expectativa mediana > yq.financial_data.targetMedianPrice

Evolução das recomendações > yq.recommendation_trend
Há 1 mês
Há 2 meses
Há 3 meses
"""
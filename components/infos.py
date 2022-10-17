from dash import html, dcc
import dash_bootstrap_components as dbc

from app import app

# =============== Layout =============== #
layout = dbc.Col([
# Seção seleção do ativo------------------
    dbc.Row([
        html.Label("Ativo: ",
                style={'font-size': 18}),
        html.Div(dcc.Dropdown(id='infos-selecao-ativo',
                              clearable=False,
                              persistence=True,
                              persistence_type='session',
                              multi=False,
                              style={'width': '100%', 'align': 'left'})),
        html.Label("Nome da empresa...",
                   id='infos-nome-empresa',
                   style={'font-size': 18, 'width': '100%'}),
        dbc.Row([
            dbc.Col([
                dbc.Label([html.Img(src='/assets/logo_padrao.png',
                                    id='infos-logo',
                                    alt='Avatar',
                                    style={'height': '80px', 'width': '80px'})
                                    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            ], width=5),
            dbc.Col([
                html.Label("Data... ",
                           id='infos-data-preco',
                           style={'font-size': 18, 'width': '100%'}),
                html.Label("R$ ...",
                           id='infos-preco',
                           style={'font-size': 18, 'width': '100%'}),
            ], width=7)
        ]),
        html.Hr()
    ])
], style={'padding': '10px'})

# ============== Callbacks ============== #
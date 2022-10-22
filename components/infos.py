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
                           style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
                html.Label("R$ ...",
                           id='infos-preco',
                           style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
            ], width=7)
        ]),
        html.Hr(),
    ]),
    

# Seção setor e informações gerais ------------------
    dbc.Row([
        html.Label("Setor X...",
                   id='infos-setor',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        html.Label("Indústria X...",
                   id='infos-industria',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        dbc.Col([
            html.Label("Valor de mercado: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Qtd funcionários: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=8),
        dbc.Col([
            html.Label("R$ X...",
                       id='infos-valor-mercado',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("X...",
                       id='infos-funcionarios',
                       style={'font-size': 18, 'width': '100%'})
        ], width=4),
        html.Hr()
    ]),
    
# Seção dividendos e payout ------------------
    dbc.Row([
        dbc.Col([
            html.Label("12 meses: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Data COM: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Payout: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=6),
        dbc.Col([
            html.Label("R$ X... / Y... %",
                       id='infos-dividendos-yield',
                       style={'font-size': 22, 'width': '100%'}),
            html.Label("Data...",
                       id='infos-data-com',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("X...%",
                       id='infos-payout',
                       style={'font-size': 18, 'width': '100%'})
        ], width=6),
        html.Hr()
    ]),

# Seção ESG ------------------------------------
    dbc.Row([
        dbc.Col([
            html.Label("ESG Total: ",
                       style={'font-size': 18, 'width': '100%', 'padding-bottom': '5px'}),
            html.Label("Ambiental: ",
                       style={'font-size': 18, 'width': '100%', 'padding-bottom': '5px'}),
            html.Label("Social: ",
                       style={'font-size': 18, 'width': '100%', 'padding-bottom': '5px'}),
            html.Label("Governança: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=6), 
        dbc.Col([
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos-esg-total',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos-esg-ambiental',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos-esg-social',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos-esg-governanca',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'})
        ], width=6),
        html.Hr()
    ]),

# Seção Polêmicas ------------------------------
    html.Label("Envolvimento em polêmicas",
               style={'font-size': 18, 'width': '100%'}),
    
    html.Label("- Polêmica 1... \n - Polêmica 2...",
               id='infos-polemicas',
               style={'font-size': 18})

], style={'padding': '10px'})

# ============== Callbacks ============== #
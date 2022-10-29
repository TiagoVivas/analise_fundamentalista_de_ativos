from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go

import yfinance as yf

from app import app
from globals import *

# ============ Layout ============ #
layout = dbc.Col([
    dbc.Row([
# Seção filtros -------------------------
        dbc.Col([
            dbc.Card([
                    dcc.Graph(id='cotacao_grafico')
                ], style={'height': '100%', 'padding': '10px'})
        ], width=9),
# Seção gráfico -------------------------
        dbc.Col([
            dbc.Card([
            html.Legend("Filtros de cotação"),
            html.Label("Período:",
                    style={'font-size': 18}),
            html.Div(dcc.Dropdown(id='cotacao_periodo',
                                    clearable=False,
                                    style={'width': '100%'},
                                    persistence=True,
                                    persistence_type='session',
                                    multi=False)),
            html.Label("Intervalo:",
                    style={'font-size': 18}),
            html.Div(dcc.Dropdown(id='cotacao_intervalo',
                                    clearable=False,
                                    style={'width': '100%'},
                                    persistence=True,
                                    persistence_type='session',
                                    multi=False)),
            #html.Label("Período de análise", 
            #        style={'font-size': 18}),
            #dcc.DatePickerRange(id='cotacao_datas',
            #                    month_format='D MMM, YY',
            #                    end_date_placeholder_text='Data...',
            #                    start_date=datetime.today() - timedelta(days=31),
            #                    end_date=datetime.today(),
            #                    updatemode='singledate',
            #                    display_format='D/M/yyyy',
            #                    style={'z-index': '100'})
            ], style={'height': '100%', 'padding': '10px'})
        ], width=3)
    ])
])

# ============ Callbacks ============ #
@app.callback(
    [
        Output('cotacao_periodo', 'options'),
        Output('cotacao_periodo', 'value'),
        Output('cotacao_intervalo', 'options'),
        Output('cotacao_intervalo', 'value')
    ],
    Input('store_ativo_selecionado', 'data')
)
def popula_filtros_cotacao(ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    lista_de_periodos = [
        {'label': '3 meses', 'value':'3mo'},
        {'label': '6 meses', 'value':'6mo'},
        {'label': '1 ano', 'value':'1y'},
        {'label': '2 anos', 'value':'2y'},
        {'label': '5 anos', 'value':'5y'},
        {'label': '10 anos', 'value':'10y'},
        {'label': 'Este ano', 'value':'ytd'},
        {'label': 'Máximo', 'value':'max'}
    ]

    lista_de_intervalos = [
        {'label': 'Diário', 'value':'1d'},
        {'label': 'Semanal', 'value':'1wk'},
        {'label': 'Mensal', 'value':'1mo'},
        {'label': 'Trimestral', 'value':'3mo'}
    ]

    return (lista_de_periodos, '1y', lista_de_intervalos, '1d')

@app.callback(
    Output('cotacao_grafico', 'figure'),
    [
        Input('cotacao_periodo', 'value'),
        Input('cotacao_intervalo', 'value')
    ],
    State('store_ativo_selecionado', 'data')
)
def atualiza_grafico_cotacao(periodo, intervalo, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    acao_yf = yf.Ticker(ativo + '.SA')
    df_precos = acao_yf.history(period=periodo,
                                interval=intervalo,
                                prepost=False,
                                auto_adjust=True,
                                actions=False)
    df_precos.reset_index(drop=False, inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_precos['Date'],
                                 open=df_precos['Open'],
                                 high=df_precos['High'],
                                 low=df_precos['Low'],
                                 close=df_precos['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=500)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig
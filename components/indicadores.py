from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
from datetime import datetime

import yfinance as yf
import yahooquery as yq

from app import app
from globals import *

# ============ Layout ============ #
layout = dbc.Col([
# Seção Indicadores de Valuation ----------------
    html.Legend("Indicadores de Valuation"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H6("P/L",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_p_l',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("P/VP",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_p_vp',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("LPA",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_lpa',
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
                html.Label(".",
                            id='indicadores_div_liq_pl',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("PL/Ativos",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_pl_ativos',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Passivos/Ativos",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_passivos_ativos',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Liquidez corrente",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_liquidez_corrente',
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
                html.Label(".",
                            id='indicadores_margem_bruta',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                html.H6("Margem líquida",
                        style={'textAlign': 'center'}),
                html.Label(".",
                            id='indicadores_margem_liquida',
                            style={'font-size': 24, 'width': '100%', 'textAlign': 'center'})
            ])
        ], width=2)
    ]),
    html.Hr()
])

# ============ Callbacks ============ #
@app.callback(
    Output('store_indicadores', 'data'),
    [
        Input('store_ativo_selecionado', 'data'),
        Input('store_financas', 'data'),
        Input('store_balanco', 'data'),
        Input('store_infos', 'data')
    ],
    State('store_indicadores', 'data')
)
def atualiza_dados_indicadores(ativo, dados_financas, dados_balanco, dados_infos, dados_indicadores):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_ind = pd.DataFrame(dados_indicadores)
    df_ind_ativo = df_ind[df_ind['ativo'] == ativo]
    if df_ind_ativo.shape[0] == 0:
        ultima_data_armazenada = ''
    else:
        ultima_data_armazenada = df_ind_ativo['data'].tolist()[0]

    acao_yq = yq.Ticker(ativo + '.SA', country='Brazil', validate=True)
    dados_price = acao_yq.price[ativo+'.SA']
    if 'regularMarketTime' in dados_price.keys():
        ultima_data_divulgada = dados_price['regularMarketTime'][0:10]
        ultima_data_divulgada = datetime.strptime(ultima_data_divulgada, "%Y-%m-%d").date()
    else:
        ultima_data_divulgada = ''

    #atualizar = (ultima_data_divulgada != '') & (ultima_data_armazenada != ultima_data_divulgada)
    atualizar = True
    if atualizar:
        df_fin = pd.DataFrame(dados_financas)
        df_fin_ativo = df_fin[(df_fin['ativo'] == ativo) & (df_fin['tipo_periodo'] == 'Trimestral')].reset_index()

        df_bal = pd.DataFrame(dados_balanco)
        df_bal_ativo = df_bal[(df_bal['ativo'] == ativo) & (df_bal['tipo_periodo'] == 'Trimestral')].reset_index()

        df_infos = pd.DataFrame(dados_infos)
        df_infos_ativo = df_infos[df_infos['ativo'] == ativo].reset_index()

        print('')
        #teste = yf.Ticker(ativo + '.SA').info
        #for chave in teste.keys():
        #    print(f"{chave}: {teste[chave]}")

        lpa = df_fin_ativo['lucro_liquido'].sum() / df_infos_ativo.loc[0, 'quantidade_acoes']
        p_l = df_infos_ativo.loc[0, 'preco'] / lpa
        patrimonio_liquido = df_bal_ativo.loc[0, 'ativo_circulante'] + df_bal_ativo.loc[0, 'ativo_nao_circulante']
        patrimonio_liquido = patrimonio_liquido - df_bal_ativo.loc[0, 'passivo_circulante'] - df_bal_ativo.loc[0, 'passivo_nao_circulante']
        p_vp = df_infos_ativo.loc[0, 'preco'] * df_infos_ativo.loc[0, 'quantidade_acoes'] / patrimonio_liquido

        #TODO: Mostrar aviso para atualizar balanço e finanças antes
        #TODO: Encontrar qtd de ações de outra forma

        print(f'Patrimonio líquido: {patrimonio_liquido}')

        estrutura_dados_indicadores = {
            'ativo': [ativo],
            'data': [ultima_data_divulgada],
            'p_l': [p_l],
            'p_vp': [p_vp],
            'lpa': [lpa],
            'divida_liquida_pl': [0],
            'pl_ativos': [0],
            'passivos_ativos': [0],
            'liquidez_corrente': [0],
            'margem_bruta': [0],
            'margem_liquida': [0]
        }

        df_append = pd.DataFrame(estrutura_dados_indicadores)

        # Remove dados anteriores
        df_ind = df_ind[(df_ind['ativo'] != ativo)]

        # Adiciona nova linha com informações atualizadas
        df_ind = pd.concat([df_ind, df_append]).reset_index(drop=True)
        df_ind.to_csv('df_indicadores.csv')

    return df_ind.to_dict()

@app.callback(
    [
        Output('indicadores_p_l', 'children'),
        Output('indicadores_p_vp', 'children'),
        Output('indicadores_lpa', 'children'),
    ],
    Input('store_indicadores', 'data'),
    State('store_ativo_selecionado', 'data')
)
def mostra_valores_indicadores(dados_indicadores, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_ind = pd.DataFrame(dados_indicadores)
    df_ind_ativo = df_ind[df_ind['ativo'] == ativo].reset_index()

    p_l = round(df_ind_ativo.loc[0, 'p_l'], 2)
    p_vp = round(df_ind_ativo.loc[0, 'p_vp'], 2)
    lpa = round(df_ind_ativo.loc[0, 'lpa'], 2)

    return (p_l, p_vp, lpa)
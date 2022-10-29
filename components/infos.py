from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import datetime
from dateutil.relativedelta import relativedelta

from app import app
from globals import *

import yfinance as yf
import yahooquery as yq 

import pdb

# =============== Layout =============== #
layout = dbc.Col([
# Seção seleção do ativo------------------
    dbc.Row([
        html.Label("Ativo: ",
                style={'font-size': 18}),
        html.Div(dcc.Dropdown(id='infos_selecao_ativo',
                              clearable=False,
                              persistence=True,
                              persistence_type='session',
                              placeholder="Selecione um ativo...",
                              multi=False,
                              style={'width': '100%', 'align': 'left'})),
        html.Label("Nome da empresa...",
                   id='infos_nome_empresa',
                   style={'font-size': 18, 'width': '100%'}),
        dbc.Row([
            dbc.Col([
                dbc.Label([html.Img(src='/assets/logo_padrao.png',
                                    id='infos_logo',
                                    alt='Avatar',
                                    style={'height': '80px', 'width': '80px'})
                                    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            ], width=5),
            dbc.Col([
                html.Label("Data... ",
                           id='infos_data_preco',
                           style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
                html.Label("R$ ...",
                           id='infos_preco',
                           style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
            ], width=7)
        ]),
        html.Hr(),
    ]),
    

# Seção setor e informações gerais ------------------
    dbc.Row([
        html.Label("Setor X...",
                   id='infos_setor',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        html.Label("Indústria X...",
                   id='infos_industria',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        dbc.Col([
            html.Label("Valor de mercado: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Qtd funcionários: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=8),
        dbc.Col([
            html.Label("R$ X...",
                       id='infos_valor_mercado',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("X...",
                       id='infos_funcionarios',
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
                       id='infos_dividendos_yield',
                       style={'font-size': 22, 'width': '100%'}),
            html.Label("Data...",
                       id='infos_data_com',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("X...%",
                       id='infos_payout',
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
                                id='infos_esg_total',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos_esg_ambiental',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos_esg_social',
                                alt='Avatar',
                                style={'height': '20px', 'width': '120px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/esg_padrao.png',
                                id='infos_esg_governanca',
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
               id='infos_polemicas',
               style={'font-size': 18})

], style={'padding': '10px'})

# ============== Callbacks ============== #
@app.callback(
    [
        Output('infos_selecao_ativo', 'options'),
        Output('infos_selecao_ativo', 'value')
    ],
    Input('store_ativos', 'data')
)
def popula_selecao_ativos(data):
    lista_ativos = data
    lista_ativos = [{'label': i, 'value': i} for i in lista_ativos]

    return (lista_ativos, None)

@app.callback(
    Output('store_infos', 'data'),
    Input('infos_selecao_ativo', 'value'),
    State('store_infos', 'data')
)
def atualiza_dados_info(ativo, dados_info):
    if ativo is None: # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate
        
    df_infos = pd.DataFrame(dados_info)
    df_infos_ativo = df_infos[df_infos['ativo'] == ativo]
    data_armazenada = df_infos_ativo['data'].values

    acao_yq = yq.Ticker(ativo + '.SA', country='Brazil', validate=True)
    dados_price = acao_yq.price[ativo+'.SA']
    data = dados_price['regularMarketTime'][0:10]

    # Precisa atualizar os dados?
    if len(data_armazenada) == 0:
        atualizar = True
    elif data_armazenada[0] != data:
        atualizar = True
    else:
        atualizar = False

    if atualizar == True:
        acao_yf = yf.Ticker(ativo + '.SA')
        dados_logo = acao_yf.info
        dados_asset_profile = acao_yq.asset_profile[ativo+'.SA']
        dados_summary_detail = acao_yq.summary_detail[ativo+'.SA']
        dados_esg_scores = acao_yq.esg_scores[ativo+'.SA']
        df_dividendos = acao_yf.actions

        if type(dados_price) == dict:
            nome = dados_price['longName'] if 'longName' in dados_price.keys() else ''
            preco = dados_price['regularMarketPrice'] if 'regularMarketPrice' in dados_price.keys() else ''
            valor_mercado = dados_price['marketCap']  if 'marketCap' in dados_price.keys() else ''
        else:
            nome = ''
            preco = ''
            valor_mercado = ''
        if type(dados_logo) == dict:
            logo = dados_logo['logo_url'] if 'logo_url' in dados_logo.keys() else ''
        else:
            logo = ''
        if type(dados_asset_profile) == dict:
            setor = dados_asset_profile['sector'] if 'sector' in dados_asset_profile.keys() else ''
            industria = dados_asset_profile['industry'] if 'industry' in dados_asset_profile.keys() else ''
            funcionarios = dados_asset_profile['fullTimeEmployees'] if 'fullTimeEmployees' in dados_asset_profile.keys() else ''
        else:
            setor = ''
            industria = ''
            funcionarios = ''
        if type(dados_summary_detail) == dict:
            data_com = dados_summary_detail['exDividendDate'][0:10] if 'exDividendDate' in dados_summary_detail.keys() else ''
            payout = dados_summary_detail['payoutRatio'] if 'payoutRatio' in dados_summary_detail.keys() else ''
        else:
            data_com = ''
            payout = ''
        if type(dados_esg_scores) == dict:
            esg_total_atual = dados_esg_scores['totalEsg'] if 'totalEsg' in dados_esg_scores.keys() else ''
            esg_total_min = dados_esg_scores['peerEsgScorePerformance']['min'] if 'peerEsgScorePerformance' in dados_esg_scores.keys() else ''
            esg_total_max = dados_esg_scores['peerEsgScorePerformance']['max'] if 'peerEsgScorePerformance' in dados_esg_scores.keys() else ''
            esg_total_med = dados_esg_scores['peerEsgScorePerformance']['avg'] if 'peerEsgScorePerformance' in dados_esg_scores.keys() else ''
            esg_ambiental_atual = dados_esg_scores['environmentScore'] if 'environmentScore' in dados_esg_scores.keys() else ''
            esg_ambiental_min = dados_esg_scores['peerEnvironmentPerformance']['min'] if 'peerEnvironmentPerformance' in dados_esg_scores.keys() else ''
            esg_ambiental_max = dados_esg_scores['peerEnvironmentPerformance']['max'] if 'peerEnvironmentPerformance' in dados_esg_scores.keys() else ''
            esg_ambiental_med = dados_esg_scores['peerEnvironmentPerformance']['avg'] if 'peerEnvironmentPerformance' in dados_esg_scores.keys() else ''
            esg_social_atual = dados_esg_scores['socialScore'] if 'socialScore' in dados_esg_scores.keys() else ''
            esg_social_min = dados_esg_scores['peerSocialPerformance']['min'] if 'peerSocialPerformance' in dados_esg_scores.keys() else ''
            esg_social_max = dados_esg_scores['peerSocialPerformance']['max'] if 'peerSocialPerformance' in dados_esg_scores.keys() else ''
            esg_social_med = dados_esg_scores['peerSocialPerformance']['avg'] if 'peerSocialPerformance' in dados_esg_scores.keys() else ''
            esg_governanca_atual = dados_esg_scores['governanceScore'] if 'governanceScore' in dados_esg_scores.keys() else ''
            esg_governanca_min = dados_esg_scores['peerGovernancePerformance']['min'] if 'peerGovernancePerformance' in dados_esg_scores.keys() else ''
            esg_governanca_max = dados_esg_scores['peerGovernancePerformance']['max'] if 'peerGovernancePerformance' in dados_esg_scores.keys() else ''
            esg_governanca_med = dados_esg_scores['peerGovernancePerformance']['avg'] if 'peerGovernancePerformance' in dados_esg_scores.keys() else ''
            polemicas = dados_esg_scores['relatedControversy'] if 'relatedControversy' in dados_esg_scores.keys() else ''
        else:
            esg_total_atual = ''
            esg_total_min = ''
            esg_total_max = ''
            esg_total_med = ''
            esg_ambiental_atual = ''
            esg_ambiental_min = ''
            esg_ambiental_max = ''
            esg_ambiental_med = ''
            esg_social_atual = ''
            esg_social_min = ''
            esg_social_max = ''
            esg_social_med = ''
            esg_governanca_atual = ''
            esg_governanca_min = ''
            esg_governanca_max = ''
            esg_governanca_med = ''
            polemicas = ''

        df_dividendos = df_dividendos.reset_index()
        df_dividendos = df_dividendos.drop(columns='Stock Splits')
        df_dividendos = df_dividendos[df_dividendos['Date'] >= (datetime.datetime.today() - relativedelta(months=12))]
        dividendos = round(df_dividendos['Dividends'].sum(), 2)
        dividendos_percent = round(100*(dividendos/preco), 2)

        # Remove dados anteriores
        df_infos = df_infos[df_infos['ativo'] != ativo]

        # Adiciona nova linha com informações atualizadas
        estrutura_dados_infos = {
            'ativo': [ativo],
            'data': [data],
            'nome': [nome],
            'logo': [logo],
            'preco': [preco],
            'setor': [setor],
            'industria': [industria],
            'valor_mercado': [valor_mercado],
            'funcionarios': [funcionarios],
            'proventos_12_meses': [dividendos],
            'div_12_meses': [dividendos_percent],
            'data_com': [data_com],
            'payout': [payout],
            'esg_total_min': [esg_total_min],
            'esg_total_max': [esg_total_max],
            'esg_total_med': [esg_total_med],
            'esg_total_atual': [esg_total_atual],
            'esg_ambiental_min': [esg_ambiental_min],
            'esg_ambiental_max': [esg_ambiental_max],
            'esg_ambiental_med': [esg_ambiental_med],
            'esg_ambiental_atual': [esg_ambiental_atual],
            'esg_social_min': [esg_social_min],
            'esg_social_max': [esg_social_max],
            'esg_social_med': [esg_social_med],
            'esg_social_atual': [esg_social_atual],
            'esg_governanca_min': [esg_governanca_min],
            'esg_governanca_max': [esg_governanca_max],
            'esg_governanca_med': [esg_governanca_med],
            'esg_governanca_atual': [esg_governanca_atual],
            'polemicas': [polemicas]
        }
        df_append_info = pd.DataFrame(estrutura_dados_infos)
        df_infos = pd.concat([df_infos, df_append_info]).reset_index(drop=True)
        df_infos.to_csv('df_infos.csv')

    return df_infos.to_dict()
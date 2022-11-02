from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import datetime
from dateutil.relativedelta import relativedelta
import os, base64, io
import urllib.request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

import yfinance as yf
import yahooquery as yq 

from app import app
from globals import *

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
        html.Label(".",
                   id='infos_nome_empresa',
                   style={'font-size': 18, 'width': '100%'}),
        dbc.Row([
            dbc.Col([
                dbc.Label([html.Img(src='/assets/logo_padrao.png',
                                    id='infos_logo',
                                    alt='Avatar',
                                    style={'height': '100%', 'width': '100%'})
                                    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            ], width=7),
            dbc.Col([
                html.Label("",
                           id='infos_data_preco',
                           style={'font-size': 18, 'width': '100%'}),
                html.Label("",
                           id='infos_preco',
                           style={'font-size': 18, 'width': '100%'}),
            ], width=5)
        ]),
        html.Hr(),
    ]),
    

# Seção setor e informações gerais ------------------
    dbc.Row([
        html.Label("Setor",
                   id='infos_setor',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        html.Label("Indústria",
                   id='infos_industria',
                   style={'font-size': 18, 'width': '100%', 'textAlign': 'center'}),
        dbc.Col([
            html.Label("Valor de mercado: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Qtd funcionários: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=8),
        dbc.Col([
            html.Label("",
                       id='infos_valor_mercado',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("",
                       id='infos_funcionarios',
                       style={'font-size': 18, 'width': '100%'})
        ], width=4),
        html.Hr()
    ]),
    
# Seção dividendos e payout ------------------
    dbc.Row([
        dbc.Col([
            html.Label("Div. 12 meses: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Data COM: ",
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("Payout: ",
                       style={'font-size': 18, 'width': '100%'})
        ], width=5),
        dbc.Col([
            html.Label("",
                       id='infos_dividendos_yield',
                       style={'font-size': 20, 'width': '100%'}),
            html.Label("",
                       id='infos_data_com',
                       style={'font-size': 18, 'width': '100%'}),
            html.Label("",
                       id='infos_payout',
                       style={'font-size': 18, 'width': '100%'})
        ], width=7),
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
        ], width=5), 
        dbc.Col([
            dbc.Label([html.Img(src='/assets/blanck.png',
                                id='infos_esg_total',
                                alt='Avatar',
                                style={'height': '25px', 'width': '180px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/blanck.png',
                                id='infos_esg_ambiental',
                                alt='Avatar',
                                style={'height': '25px', 'width': '180px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/blanck.png',
                                id='infos_esg_social',
                                alt='Avatar',
                                style={'height': '25px', 'width': '180px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
            dbc.Label([html.Img(src='/assets/blanck.png',
                                id='infos_esg_governanca',
                                alt='Avatar',
                                style={'height': '25px', 'width': '180px'})
                                ], style={'background-color': 'transparent', 'border-color': 'transparent'})
        ], width=7),
        html.Hr()
    ]),

# Seção Polêmicas ------------------------------
    html.Label("Envolvimento em polêmicas",
               style={'font-size': 18, 'width': '100%'}),
    
    html.Label("",
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
    [
        Output('store_infos', 'data'),
        Output('store_ativo_selecionado', 'data')
    ],
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

    return (df_infos.to_dict(), ativo)

@app.callback(
    [
        Output('infos_nome_empresa', 'children'),
        Output('infos_data_preco', 'children'),
        Output('infos_preco', 'children'),
        Output('infos_logo', 'src'),
        Output('infos_setor', 'children'),
        Output('infos_industria', 'children'),
        Output('infos_valor_mercado', 'children'),
        Output('infos_funcionarios', 'children'),
        Output('infos_dividendos_yield', 'children'),
        Output('infos_data_com', 'children'),
        Output('infos_payout', 'children'),
        Output('infos_esg_total', 'src'),
        Output('infos_esg_ambiental', 'src'),
        Output('infos_esg_social', 'src'),
        Output('infos_esg_governanca', 'src'),
        Output('infos_polemicas', 'children')
    ],
    Input('store_infos', 'data'),
    State('infos_selecao_ativo', 'value')
)
def mostra_valores_infos(dados_info, ativo):
    if ativo is None: # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_infos = pd.DataFrame(dados_info)
    df_infos_ativo = df_infos[df_infos['ativo'] == ativo]

    # Nome da empresa
    nome = df_infos_ativo['nome'].values
    nome = nome[0] if len(nome) != 0 else ''

    # Data do último negócio
    data = df_infos_ativo['data'].values
    if len(data) != 0:
        data = data[0]
        data = data[8:10] + '/' + data[5:7] + '/' + data[0:4]
    else:
        data = ''

    # Último preço de mercado
    preco = df_infos_ativo['preco'].values
    preco = preco[0] if len(preco) != 0 else ''
    preco = 'R$ ' + str(round(preco, 2)).replace('.', ',')

    # Logo da empresa
    logo = f"logo_{ativo}.png"
    if logo not in os.listdir('assets/'):
        try:
            url_logo = df_infos_ativo['logo'].values
            url_logo = url_logo[0] if len(url_logo) != 0 else ''
            urllib.request.urlretrieve(url_logo, f"assets/{logo}")
        except:
            logo = 'logo_padrao.png'

    # Setor de atuação
    setor = df_infos_ativo['setor'].values
    setor = setor[0] if len(setor) != 0 else ''

    # Indústria de atuação
    industria = df_infos_ativo['industria'].values
    industria = industria[0] if len(industria) != 0 else ''

    # Valor de mercado
    valor_mercado = df_infos_ativo['valor_mercado'].values
    valor_mercado = valor_mercado[0] if len(valor_mercado) != 0 else ''
    valor_mercado = 'R$ ' + str(round(valor_mercado/1000000000, 1)).replace('.', ',') + ' B'

    # Qtd de funcionários
    funcionarios = df_infos_ativo['funcionarios'].values
    funcionarios = funcionarios[0] if len(funcionarios) != 0 else ''

    # Dividendos
    dividendos = df_infos_ativo['proventos_12_meses'].values
    dividendos = dividendos[0] if len(dividendos) != 0 else ''

    div_yield = df_infos_ativo['div_12_meses'].values
    div_yield = div_yield[0] if len(div_yield) != 0 else ''

    dividendos = f"R$ {str(round(dividendos,2)).replace('.', ',')} / {str(round(div_yield, 2)).replace('.', ',')} %"

    # Data COM do último provento
    data_com = df_infos_ativo['data_com'].values
    if len(data_com) != 0:
        data_com = data_com[0]
        data_com = data_com[8:10] + '/' + data_com[5:7] + '/' + data_com[0:4]
    else:
        data_com = ''

    # Payout
    payout = df_infos_ativo['payout'].values
    payout = payout[0] if len(payout) != 0 else ''
    payout = str(100*round(payout, 2)).replace('.', ',') + ' %'

    # ESG total
    esg_total = df_infos_ativo['esg_total_atual'].values
    esg_total = esg_total[0] if len(esg_total) != 0 else -1
    esg_total = -1 if (esg_total == '') | (math.isnan(esg_total)) else esg_total
    esg_total_min = df_infos_ativo['esg_total_min'].values
    esg_total_min = esg_total_min[0] if len(esg_total_min) != 0 else 0
    esg_total_min = -1 if (esg_total_min == '') | (math.isnan(esg_total_min)) else esg_total_min
    esg_total_max = df_infos_ativo['esg_total_max'].values
    esg_total_max = esg_total_max[0] if len(esg_total_max) != 0 else 1
    esg_total_max = -1 if (esg_total_max == '') | (math.isnan(esg_total_max)) else esg_total_max
    esg_total_med = df_infos_ativo['esg_total_med'].values
    esg_total_med = esg_total_med[0] if len(esg_total_med) != 0 else -1
    esg_total_med = -1 if (esg_total_med == '') | (math.isnan(esg_total_med)) else esg_total_med

    fig, ax = plt.subplots(figsize=(1.5, 0.3))
    p1 = ax.barh(0, [esg_total_min, esg_total_max])
    p2 = ax.scatter(esg_total_med - esg_total_min, 0, color = 'orange', marker = '|', s=150)
    p3 = ax.scatter(esg_total - esg_total_min, 0, color='white', marker=6, s=260)
    ax.axis('off')
    fig.patch.set_facecolor('#F0F0F0')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()
    img_data.seek(0)
    esg_total_img = 'data:image/png;base64,' + base64.b64encode(img_data.read()).decode('ascii')

    # ESG ambiental
    esg_ambiental = df_infos_ativo['esg_ambiental_atual'].values
    esg_ambiental = esg_ambiental[0] if len(esg_ambiental) != 0 else -1
    esg_ambiental = -1 if (esg_ambiental == '') | (math.isnan(esg_ambiental)) else esg_ambiental
    esg_ambiental_min = df_infos_ativo['esg_ambiental_min'].values
    esg_ambiental_min = esg_ambiental_min[0] if len(esg_ambiental_min) != 0 else 0
    esg_ambiental_min = -1 if (esg_ambiental_min == '') | (math.isnan(esg_ambiental_min)) else esg_ambiental_min
    esg_ambiental_max = df_infos_ativo['esg_ambiental_max'].values
    esg_ambiental_max = esg_ambiental_max[0] if len(esg_ambiental_max) != 0 else 1
    esg_ambiental_max = -1 if (esg_ambiental_max == '') | (math.isnan(esg_ambiental_max)) else esg_ambiental_max
    esg_ambiental_med = df_infos_ativo['esg_ambiental_med'].values
    esg_ambiental_med = esg_ambiental_med[0] if len(esg_ambiental_med) != 0 else -1
    esg_ambiental_med = -1 if (esg_ambiental_med == '') | (math.isnan(esg_ambiental_med)) else esg_ambiental_med

    fig, ax = plt.subplots(figsize=(1.5, 0.3))
    p1 = ax.barh(0, [esg_ambiental_min, esg_ambiental_max])
    p2 = ax.scatter(esg_ambiental_med - esg_ambiental_min, 0, color = 'orange', marker = '|', s=150)
    p3 = ax.scatter(esg_ambiental - esg_ambiental_min, 0, color='white', marker=6, s=260)
    ax.axis('off')
    fig.patch.set_facecolor('#F0F0F0')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()
    img_data.seek(0)
    esg_ambiental_img = 'data:image/png;base64,' + base64.b64encode(img_data.read()).decode('ascii')

    # ESG social
    esg_social = df_infos_ativo['esg_social_atual'].values
    esg_social = esg_social[0] if len(esg_social) != 0 else -1
    esg_social = -1 if (esg_social == '') | (math.isnan(esg_social)) else esg_social
    esg_social_min = df_infos_ativo['esg_social_min'].values
    esg_social_min = esg_social_min[0] if len(esg_social_min) != 0 else 0
    esg_social_min = -1 if (esg_social_min == '') | (math.isnan(esg_social_min)) else esg_social_min
    esg_social_max = df_infos_ativo['esg_social_max'].values
    esg_social_max = esg_social_max[0] if len(esg_social_max) != 0 else 1
    esg_social_max = -1 if (esg_social_max == '') | (math.isnan(esg_social_max)) else esg_social_max
    esg_social_med = df_infos_ativo['esg_social_med'].values
    esg_social_med = esg_social_med[0] if len(esg_social_med) != 0 else -1
    esg_social_med = -1 if (esg_social_med == '') | (math.isnan(esg_social_med)) else esg_social_med

    fig, ax = plt.subplots(figsize=(1.5, 0.3))
    p1 = ax.barh(0, [esg_social_min, esg_social_max])
    p2 = ax.scatter(esg_social_med - esg_social_min, 0, color = 'orange', marker = '|', s=150)
    p3 = ax.scatter(esg_social - esg_social_min, 0, color='white', marker=6, s=260)
    ax.axis('off')
    fig.patch.set_facecolor('#F0F0F0')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()
    img_data.seek(0)
    esg_social_img = 'data:image/png;base64,' + base64.b64encode(img_data.read()).decode('ascii')

    # ESG governanca
    esg_governanca = df_infos_ativo['esg_governanca_atual'].values
    esg_governanca = esg_governanca[0] if len(esg_governanca) != 0 else -1
    esg_governanca = -1 if (esg_governanca == '') | (math.isnan(esg_governanca)) else esg_governanca
    esg_governanca_min = df_infos_ativo['esg_governanca_min'].values
    esg_governanca_min = esg_governanca_min[0] if len(esg_governanca_min) != 0 else 0
    esg_governanca_min = -1 if (esg_governanca_min == '') | (math.isnan(esg_governanca_min)) else esg_governanca_min
    esg_governanca_max = df_infos_ativo['esg_governanca_max'].values
    esg_governanca_max = esg_governanca_max[0] if len(esg_governanca_max) != 0 else 1
    esg_governanca_max = -1 if (esg_governanca_max == '') | (math.isnan(esg_governanca_max)) else esg_governanca_max
    esg_governanca_med = df_infos_ativo['esg_governanca_med'].values
    esg_governanca_med = esg_governanca_med[0] if len(esg_governanca_med) != 0 else -1
    esg_governanca_med = -1 if (esg_governanca_med == '') | (math.isnan(esg_governanca_med)) else esg_governanca_med

    fig, ax = plt.subplots(figsize=(1.5, 0.3))
    p1 = ax.barh(0, [esg_governanca_min, esg_governanca_max])
    p2 = ax.scatter(esg_governanca_med - esg_governanca_min, 0, color = 'orange', marker = '|', s=150)
    p3 = ax.scatter(esg_governanca - esg_governanca_min, 0, color='white', marker=6, s=260)
    ax.axis('off')
    fig.patch.set_facecolor('#F0F0F0')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()
    img_data.seek(0)
    esg_governanca_img = 'data:image/png;base64,' + base64.b64encode(img_data.read()).decode('ascii')

    # Polêmicas
    polemicas = df_infos_ativo['polemicas'].values
    polemicas = polemicas.tolist()
    polemicas = polemicas[0]
    if polemicas == None:
        polemicas = ''
    elif type(polemicas) != list: # Na primeira atualização vem com formato de lista e não de string
        polemicas = polemicas.replace('[', '').replace(']', '')
        polemicas = polemicas.split(',')
    polemicas = ' <=> ' + ' <=> '.join(polemicas)
    
    return (nome, data, preco, f"assets/{logo}", setor, industria, valor_mercado, funcionarios, dividendos, data_com, payout, esg_total_img, esg_ambiental_img, esg_social_img, esg_governanca_img, polemicas)
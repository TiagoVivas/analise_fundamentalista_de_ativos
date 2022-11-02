from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

import yfinance as yf
import yahooquery as yq

from app import app
from globals import *

dados_fin = {
    ' ': ["Receita total",
          " ",
          "Custo prod. vend.",
          "Despesas adm/vendas",
          "P&D",
          "Despesas com juros",
          " ",
          "Ebit",
          "Lucro bruto",
          "Lucro antes impostos",
          "Lucro líquido"],
    'Q4': ['' for i in range(11)],
    'Q3': ['' for i in range(11)],
    'Q2': ['' for i in range(11)],
    'Q1': ['' for i in range(11)]
}
df_fin = pd.DataFrame(dados_fin)

# ============ Layout ============ #
layout = dbc.Col([
# Seção de filtros -------------------------------------------
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend("Filtro de finanças"),
                dcc.RadioItems(options=["Trimestral", "Anual"],
                               value="Trimestral",
                               id='financas_filtro',
                               persistence=True,
                               persistence_type='session',
                               labelStyle={'display': 'block'},
                               style={'font-size': 18})
            ], style={'height': '100%', 'padding': '10px'})
        ], width=4)
    ], style={'padding-bottom': '10px'}),

    dbc.Row([
# Seção de tabela de dados -----------------------------------
        dbc.Col([
            dbc.Card([
                dash_table.DataTable(df_fin.to_dict('records'),
                                     [{'name': i, 'id': i} for i in df_fin.columns],
                                     id='financas_tabela')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=8),
# Seção de gráficos -----------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='financas_grafico', style={'height': '300px'})
            ], style={'height': '100%', 'padding': '10px'})
        ], width=4)
    ])
])

# ============ Callbacks ============ #
@app.callback(
    Output('financas_filtro', 'value'),
    Input('store_ativo_selecionado', 'data')
)
def popula_filtro_periodo_financas(ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    return 'Trimestral'

@app.callback(
    Output('store_financas', 'data'),
    Input('financas_filtro', 'value'),
    [
        State('store_financas', 'data'),
        State('store_ativo_selecionado', 'data')
    ]
)
def atualiza_dados_financas(filtro_periodo, dados_financas, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_fin = pd.DataFrame(dados_financas)
    df_fin_ativo = df_fin[(df_fin['ativo'] == ativo) & (df_fin['tipo_periodo'] == filtro_periodo)]
    if df_fin_ativo.shape[0] == 0:
        ultima_data_armazenada = ''
    else:
        ultima_data_armazenada = df_fin_ativo['data'].tolist()[0]

    acao_yq = yq.Ticker(ativo + '.SA', country='Brazil', validate=True)
    df_data = acao_yq.cash_flow(frequency='q' if filtro_periodo == 'Trimestral' else 'a', trailing=False)
    ultima_data_divulgada = max(df_data.reset_index()['asOfDate']).date().strftime("%Y-%m-%d")

    atualizar = ultima_data_armazenada != ultima_data_divulgada
    if atualizar:
        acao_yf = yf.Ticker(ativo + '.SA')
        if filtro_periodo == 'Trimestral':
            df_fin_novo = acao_yf.quarterly_financials
        else:
            df_fin_novo = acao_yf.financials
        datas_existentes = df_fin_novo.columns.tolist()

        chave = []
        ativos = []
        tipo_periodo = []
        datas = []
        receita_total = []
        custo_produtos_vendidos = []
        despesas_adm_vendas = []
        pesquisa_desenvolvimento = []
        despesas_juros = []
        ebit = []
        lucro_bruto = []
        lucro_antes_impostos = []
        lucro_liquido = []
        for data in datas_existentes:
            chave.append(ativo+filtro_periodo)
            ativos.append(ativo)
            tipo_periodo.append(filtro_periodo)
            datas.append(data.date().strftime("%Y-%m-%d"))
            receita_total.append(df_fin_novo.loc['Total Revenue', data])
            custo_produtos_vendidos.append(df_fin_novo.loc['Cost Of Revenue', data])
            despesas_adm_vendas.append(df_fin_novo.loc['Selling General Administrative', data])
            pesquisa_desenvolvimento.append(df_fin_novo.loc['Research Development', data])
            despesas_juros.append(df_fin_novo.loc['Interest Expense', data])
            ebit.append(df_fin_novo.loc['Ebit', data])
            lucro_bruto.append(df_fin_novo.loc['Gross Profit', data])
            lucro_antes_impostos.append(df_fin_novo.loc['Income Before Tax', data])
            lucro_liquido.append(df_fin_novo.loc['Net Income', data])

        dados_fin = {
            'chave': chave,
            'ativo': ativos,
            'tipo_periodo': tipo_periodo,
            'data': datas,
            'receita_total': receita_total,
            'custo_produtos_vendidos': custo_produtos_vendidos,
            'despesas_adm_vendas': despesas_adm_vendas,
            'pesquisa_desenvolvimento': pesquisa_desenvolvimento,
            'despesas_juros': despesas_juros,
            'ebit': ebit,
            'lucro_bruto': lucro_bruto,
            'lucro_antes_impostos': lucro_antes_impostos,
            'lucro_liquido': lucro_liquido
        }
        df_append = pd.DataFrame(dados_fin)

        # Remove dados anteriores
        df_fin = df_fin[(df_fin['chave'] != ativo+filtro_periodo)]

        # Adiciona nova linha com informações atualizadas
        df_fin = pd.concat([df_fin, df_append]).reset_index(drop=True)
        df_fin.to_csv('df_financas.csv')

    return df_fin.to_dict()

@app.callback(
    [
        Output('financas_tabela', 'data'),
        Output('financas_tabela', 'columns')
    ],
    Input('store_financas', 'data'),
    [
        State('financas_filtro', 'value'),
        State('store_ativo_selecionado', 'data')
    ]
)
def mostra_valores_financas(dados_financas, filtro_periodo, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_fin = pd.DataFrame(dados_financas)
    df_fin_ativo = df_fin[(df_fin['ativo'] == ativo) & (df_fin['tipo_periodo'] == filtro_periodo)]
    datas = df_fin_ativo['data'].tolist()

    itens = [
        "Receita total",
        " ",
        "Custo prod. vend.", "Despesas adm/vendas", 
        "P&D", "Despesas com juros",
        " ",
        "Ebit", "Lucro bruto", 
        "Lucro antes impostos", "Lucro líquido"
    ]

    dados = []
    for data in datas:
        df = df_fin_ativo[df_fin_ativo['data'] == data].reset_index()
        dados.append(
            [
                str(round(df.loc[0, 'receita_total']/1000000, 0)),
                "",
                str(round(df.loc[0, 'custo_produtos_vendidos']/1000000, 0)), 
                str(round(df.loc[0, 'despesas_adm_vendas']/1000000, 0)),
                str(round(df.loc[0, 'pesquisa_desenvolvimento']/1000000, 0)), 
                str(round(df.loc[0, 'despesas_juros']/-1000000, 0)),
                "",
                str(round(df.loc[0, 'ebit']/1000000, 0)), 
                str(round(df.loc[0, 'lucro_bruto']/1000000, 0)), 
                str(round(df.loc[0, 'lucro_antes_impostos']/1000000, 0)), 
                str(round(df.loc[0, 'lucro_liquido']/1000000, 0))
            ]
        )

    dados_fin = {
        '(Em milhões de R$)': itens,
        datetime.strptime(datas[0], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[0],
        datetime.strptime(datas[1], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[1],
        datetime.strptime(datas[2], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[2],
        datetime.strptime(datas[3], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[3],
    }
    df_fin = pd.DataFrame(dados_fin)
    
    return (df_fin.to_dict('records'), [{'name': i, 'id': i} for i in df_fin.columns])

@app.callback(
    Output('financas_grafico', 'figure'),
    Input('financas_tabela', 'active_cell'),
    [
        State('store_ativo_selecionado', 'data'),
        State('store_financas', 'data'),
        State('financas_filtro', 'value')
    ]
)
def atualiza_grafico_financas(celula_selecionada, ativo, dados_financas, filtro_periodo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_fin = pd.DataFrame(dados_financas)
    df_fin_ativo = df_fin[(df_fin['ativo'] == ativo) & (df_fin['tipo_periodo'] == filtro_periodo)]

    fig = go.Figure()

    if celula_selecionada == None:
        fig = go.Figure()
    elif celula_selecionada['row'] == 0:
        df_fin_ativo = df_fin_ativo[['data', 'receita_total']]
        fig = px.line(df_fin_ativo, x='data', y='receita_total', title = ativo + ' - Receita Total')
    elif celula_selecionada['row'] == 2:
        df_fin_ativo = df_fin_ativo[['data', 'custo_produtos_vendidos']]
        fig = px.line(df_fin_ativo, x='data', y='custo_produtos_vendidos', title = ativo + ' - Custo Prod. Vend.')
    elif celula_selecionada['row'] == 3:
        df_fin_ativo = df_fin_ativo[['data', 'despesas_adm_vendas']]
        fig = px.line(df_fin_ativo, x='data', y='despesas_adm_vendas', title = ativo + ' - Despesas adm e vendas')
    elif celula_selecionada['row'] == 4:
        df_fin_ativo = df_fin_ativo[['data', 'pesquisa_desenvolvimento']]
        fig = px.line(df_fin_ativo, x='data', y='pesquisa_desenvolvimento', title = ativo + ' - P&D')
    elif celula_selecionada['row'] == 5:
        df_fin_ativo = df_fin_ativo[['data', 'despesas_juros']]
        df_fin_ativo['despesas_juros'] = abs(df_fin_ativo['despesas_juros'])
        fig = px.line(df_fin_ativo, x='data', y='despesas_juros', title = ativo + ' - Despesas com juros')
    elif celula_selecionada['row'] == 7:
        df_fin_ativo = df_fin_ativo[['data', 'ebit']]
        fig = px.line(df_fin_ativo, x='data', y='ebit', title = ativo + ' - EBIT')
    elif celula_selecionada['row'] == 8:
        df_fin_ativo = df_fin_ativo[['data', 'lucro_bruto']]
        fig = px.line(df_fin_ativo, x='data', y='lucro_bruto', title = ativo + ' - Lucro bruto')
    elif celula_selecionada['row'] == 9:
        df_fin_ativo = df_fin_ativo[['data', 'lucro_antes_impostos']]
        fig = px.line(df_fin_ativo, x='data', y='lucro_antes_impostos', title = ativo + ' - Lucro antes de impostos')
    elif celula_selecionada['row'] == 10:
        df_fin_ativo = df_fin_ativo[['data', 'lucro_liquido']]
        fig = px.line(df_fin_ativo, x='data', y='lucro_liquido', title = ativo + ' - Lucro líquido')

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=350)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

"""
Margem bruta > yq.financial_data.grossMargins
Margem operacional > yq.financial_data.operatingMargins
Margem líquida > yq.financial_data.profitMargins
"""
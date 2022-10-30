from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import plotly.graph_objects as go

import yfinance as yf
import yahooquery as yq

from app import app
from globals import *

dados_fin = {
    ' ': ["Receita total",
          " ",
          "Custo dos produtos vendidos",
          "Despesas adm e vendas",
          "Pesquisa e desenvolvimento",
          "Despesas com juros",
          " ",
          "Ebit",
          "Lucro bruto",
          "Lucro antes dos impostos",
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
        ], width=7),
# Seção de gráficos -----------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='financas_grafico')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=5)
    ])
])

# ============ Callbacks ============ #
@app.callback(
    Output('store_financas', 'data'),
    [
        Input('store_ativo_selecionado', 'data'),
        Input('financas_filtro', 'value')
    ],
    State('store_financas', 'data'),
)
def atualiza_dados_financas(ativo, filtro_periodo, dados_financas):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_fin = pd.DataFrame(dados_financas)
    df_fin_ativo = df_fin[(df_fin['ativo'] == ativo) & (df_fin['tipo_periodo'] == filtro_periodo)]
    if df_fin_ativo.shape[0] == 0:
        ultima_data_armazenada = ''
    else:
        ultima_data_armazenada = df_fin_ativo['data'].tolist()[0]

    acao_yq = yq.Ticker(ativo + '.SA', country='Brazil', validate=True)
    if filtro_periodo == 'Trimestral':
        df_data = acao_yq.cash_flow(frequency='q', trailing=False)
    else:
        df_data = acao_yq.cash_flow(frequency='a', trailing=False)
    ultima_data_divulgada = max(df_data.reset_index()['asOfDate']).date().strftime("%Y-%m-%d")

    atualizar = ultima_data_armazenada != ultima_data_divulgada
    if atualizar:
        print("Atualizando...")
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
            despesas_juros.append(-df_fin_novo.loc['Interest Expense', data])
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

        print("Atualizado!!!")
    else:
        print("Não precisa atualizar")

    return df_fin.to_dict()

@app.callback(
    [
        Output('financas_tabela', 'data'),
        Output('financas_tabela', 'columns'),
        Output('financas_grafico', 'figure')
    ],
    Input('store_ativo_selecionado', 'data'),
    State('financas_filtro', 'value')
)
def function(ativo, periodo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    dados_fin = {
        ' ': ["Receita total",
            " ",
            "Custo dos produtos vendidos",
            "Despesas adm e vendas",
            "Pesquisa e desenvolvimento",
            "Despesas com juros",
            " ",
            "Ebit",
            "Lucro bruto",
            "Lucro antes dos impostos",
            "Lucro líquido"],
        'Q5': [i for i in range(11)],
        'Q6': [i for i in range(11)],
        'Q7': [i for i in range(11)],
        'Q8': [i for i in range(11)]
    }
    df_fin = pd.DataFrame(dados_fin)

    fig = go.Figure()
    
    return (df_fin.to_dict('records'), [{'name': i, 'id': i} for i in df_fin.columns], fig)

"""
Receita total > Total Revenue

Custo dos produto vendidos > Cost Of Revenue
Despesas com vendas, gerais e adm > Selling General Administrative
Custo com pesquisa e desenvolvimento > Research Development
Despesas com juros > Interest Expense

Ebit (receita total - custo dos produtos vendidos) > Ebit
Lucro bruto > Gross Profit
Lucro antes dos impostos > Income Before Tax
Lucro líquido > Net Income

Margem bruta > yq.financial_data.grossMargins
Margem operacional > yq.financial_data.operatingMargins
Margem líquida > yq.financial_data.profitMargins
"""
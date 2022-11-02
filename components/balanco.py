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

dados = {
    ' ': ["ATIVO CIRCULANTE",
          "  Aplicações financeiras",
          "  Caixa",
          "  Contas a receber",
          "  Estoque",
          "ATIVO NÃO CIRCULANTE",
          "  Investimentos",
          "  Imobilizado",
          "  Intangível",
          " ",
          "PASSIVO CIRCULANTE",
          "  Dívidas de curto prazo",
          "  Fornecedores",
          "PASSIVO NÃO CIRCULANTE",
          "  Dívidas de longo prazo"],
    'Q4': [i for i in range(15)],
    'Q3': [i for i in range(15)],
    'Q2': [i for i in range(15)],
    'Q1': [i for i in range(15)],
}
df_balanco = pd.DataFrame(dados)

# ============ Layout ============ #
layout = dbc.Col([
    # Seção de filtros -------------------------------------------
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend("Filtro de balanço"),
                dcc.RadioItems(options=["Trimestral", "Anual"],
                               value="Trimestral",
                               id='balanco_filtro',
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
                dash_table.DataTable(df_balanco.to_dict('records'),
                                     [{'name': i, 'id': i} for i in df_balanco.columns],
                                     id='balanco_tabela',
                                     style_data_conditional=[
                                        {
                                            "if": {"row_index": 0},
                                            "fontWeight": "bold",
                                        },
                                        {
                                            "if": {"row_index": 5},
                                            "fontWeight": "bold",
                                        },
                                        {
                                            "if": {"row_index": 10},
                                            "fontWeight": "bold",
                                        },
                                        {
                                            "if": {"row_index": 13},
                                            "fontWeight": "bold",
                                        }
                                     ],)
            ], style={'height': '100%', 'padding': '10px'})
        ], width=7),
# Seção de gráficos -----------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='balanco_grafico')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=5)
    ])
])

# ============ Callbacks ============ #
@app.callback(
    Output('balanco_filtro', 'value'),
    Input('store_ativo_selecionado', 'data')
)
def popula_filtro_periodo_balanco(ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    return 'Trimestral'

@app.callback(
    Output('store_balanco', 'data'),
    Input('balanco_filtro', 'value'),
    [
        State('store_balanco', 'data'),
        State('store_ativo_selecionado', 'data')
    ]
)
def atualiza_dados_balanco(filtro_periodo, dados_balanco, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_bal = pd.DataFrame(dados_balanco)
    df_bal_ativo = df_bal[(df_bal['ativo'] == ativo) & (df_bal['tipo_periodo'] == filtro_periodo)]
    if df_bal_ativo.shape[0] == 0:
        ultima_data_armazenada = ''
    else:
        ultima_data_armazenada = df_bal_ativo['data'].tolist()[0]

    acao_yq = yq.Ticker(ativo + '.SA', country='Brazil', validate=True)
    df_data = acao_yq.balance_sheet(frequency='q' if filtro_periodo == 'Trimestral' else 'a', trailing=False)
    ultima_data_divulgada = max(df_data.reset_index()['asOfDate']).date().strftime("%Y-%m-%d")

    atualizar = ultima_data_armazenada != ultima_data_divulgada
    if atualizar:
        acao_yf = yf.Ticker(ativo + '.SA')
        if filtro_periodo == 'Trimestral':
            df_bal_novo = acao_yf.quarterly_balance_sheet
        else:
            df_bal_novo = acao_yf.balance_sheet
        datas_existentes = df_bal_novo.columns.tolist()

        chave = []
        ativos = []
        tipo_periodo = []
        datas = []
        ativo_circulante = []
        aplicacoes = []
        caixa = []
        contas_a_receber = []
        estoque = []
        ativo_nao_circulante = []
        investimentos = []
        imobilizado = []
        intangivel = []
        passivo_circulante = []
        dividas_curto_prazo = []
        fornecedores = []
        passivo_nao_circulante = []
        dividas_longo_prazo = []
        for data in datas_existentes:
            chave.append(ativo+filtro_periodo)
            ativos.append(ativo)
            tipo_periodo.append(filtro_periodo)
            datas.append(data.date().strftime("%Y-%m-%d"))
            ativo_circulante.append(df_bal_novo.loc['Total Current Assets', data])
            aplicacoes.append(df_bal_novo.loc['Short Term Investments', data])
            caixa.append(df_bal_novo.loc['Cash', data])
            contas_a_receber.append(df_bal_novo.loc['Net Receivables', data])
            estoque.append(df_bal_novo.loc['Inventory', data])
            ativo_nao_circulante.append(df_bal_novo.loc['Total Assets', data] - df_bal_novo.loc['Total Current Assets', data])
            investimentos.append(df_bal_novo.loc['Long Term Investments', data])
            imobilizado.append(df_bal_novo.loc['Property Plant Equipment', data])
            intangivel.append(df_bal_novo.loc['Intangible Assets', data])
            passivo_circulante.append(df_bal_novo.loc['Total Current Liabilities', data])
            dividas_curto_prazo.append(df_bal_novo.loc['Short Long Term Debt', data])
            fornecedores.append(df_bal_novo.loc['Accounts Payable', data])
            passivo_nao_circulante.append(df_bal_novo.loc['Total Liab', data] - df_bal_novo.loc['Total Current Liabilities', data])
            dividas_longo_prazo.append(df_bal_novo.loc['Long Term Debt', data])

        dados_bal = {
            'chave': chave,
            'ativo': ativos,
            'tipo_periodo': tipo_periodo,
            'data': datas,
            'ativo_circulante': ativo_circulante,
            'aplicacoes': aplicacoes,
            'caixa': caixa,
            'contas_a_receber': contas_a_receber,
            'estoque': estoque,
            'ativo_nao_circulante': ativo_nao_circulante,
            'investimentos': investimentos,
            'imobilizado': imobilizado,
            'intangivel': intangivel,
            'passivo_circulante': passivo_circulante,
            'dividas_curto_prazo': dividas_curto_prazo,
            'fornecedores': fornecedores,
            'passivo_nao_circulante': passivo_nao_circulante,
            'dividas_longo_prazo': dividas_longo_prazo
        }
        df_append = pd.DataFrame(dados_bal)

        # Remove dados anteriores
        df_bal = df_bal[(df_bal['chave'] != ativo+filtro_periodo)]

        # Adiciona nova linha com informações atualizadas
        df_bal = pd.concat([df_bal, df_append]).reset_index(drop=True)
        df_bal.to_csv('df_balanco.csv')

    return df_bal.to_dict()

@app.callback(
    [
        Output('balanco_tabela', 'data'),
        Output('balanco_tabela', 'columns')
    ],
    Input('store_balanco', 'data'),
    [
        State('balanco_filtro', 'value'),
        State('store_ativo_selecionado', 'data')
    ]
)
def mostra_valores_balanco(dados_balanco, filtro_periodo, ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_bal = pd.DataFrame(dados_balanco)
    df_bal_ativo = df_bal[(df_bal['ativo'] == ativo) & (df_bal['tipo_periodo'] == filtro_periodo)]
    datas = df_bal_ativo['data'].tolist()

    itens = [
        "ATIVO CIRCULANTE",
        "Aplicações",
        "Caixa",
        "Contas a receber",
        "Estoque",
        "ATIVO NÃO CIRCULANTE",
        "Investimentos",
        "Imobilizado",
        "Intangível",
        " ",
        "PASSIVO CIRCULANTE",
        "Dívidas curto prazo",
        "Fornecedores",
        "PASSIVO NÃO CIRCULANTE",
        "Dívidas longo prazo"
    ]

    dados = []
    for data in datas:
        df = df_bal_ativo[df_bal_ativo['data'] == data].reset_index()
        dados.append(
            [
                str(round(df.loc[0, 'ativo_circulante']/1000000, 0)),
                str(round(df.loc[0, 'aplicacoes']/1000000, 0)),
                str(round(df.loc[0, 'caixa']/1000000, 0)),
                str(round(df.loc[0, 'contas_a_receber']/1000000, 0)),
                str(round(df.loc[0, 'estoque']/1000000, 0)),
                str(round(df.loc[0, 'ativo_nao_circulante']/1000000, 0)),
                str(round(df.loc[0, 'investimentos']/1000000, 0)),
                str(round(df.loc[0, 'imobilizado']/1000000, 0)),
                str(round(df.loc[0, 'intangivel']/1000000, 0)),
                "",
                str(round(df.loc[0, 'passivo_circulante']/1000000, 0)),
                str(round(df.loc[0, 'dividas_curto_prazo']/1000000, 0)),
                str(round(df.loc[0, 'fornecedores']/1000000, 0)),
                str(round(df.loc[0, 'passivo_nao_circulante']/1000000, 0)),
                str(round(df.loc[0, 'dividas_longo_prazo']/1000000, 0))
            ]
        )

    dados_bal = {
        '(Em milhões de R$)': itens,
        datetime.strptime(datas[0], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[0],
        datetime.strptime(datas[1], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[1],
        datetime.strptime(datas[2], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[2],
        datetime.strptime(datas[3], "%Y-%m-%d").date().strftime("%d/%m/%y"): dados[3],
    }
    df_bal = pd.DataFrame(dados_bal)
    
    return (df_bal.to_dict('records'), [{'name': i, 'id': i} for i in df_bal.columns])

@app.callback(
    Output('balanco_grafico', 'figure'),
    Input('balanco_tabela', 'active_cell'),
    [
        State('store_ativo_selecionado', 'data'),
        State('store_balanco', 'data'),
        State('balanco_filtro', 'value')
    ]
)
def atualiza_grafico_financas(celula_selecionada, ativo, dados_balanco, filtro_periodo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    df_bal = pd.DataFrame(dados_balanco)
    df_bal_ativo = df_bal[(df_bal['ativo'] == ativo) & (df_bal['tipo_periodo'] == filtro_periodo)]

    fig = go.Figure()

    if celula_selecionada == None:
        fig = go.Figure()
    elif celula_selecionada['row'] == 0:
        df_bal_ativo = df_bal_ativo[['data', 'ativo_circulante']]
        fig = px.line(df_bal_ativo, x='data', y='ativo_circulante', title = ativo + ' - Ativo Circulante')
    elif celula_selecionada['row'] == 1:
        df_bal_ativo = df_bal_ativo[['data', 'aplicacoes']]
        fig = px.line(df_bal_ativo, x='data', y='aplicacoes', title = ativo + ' - Aplicações financeiras')
    elif celula_selecionada['row'] == 2:
        df_bal_ativo = df_bal_ativo[['data', 'caixa']]
        fig = px.line(df_bal_ativo, x='data', y='caixa', title = ativo + ' - Caixa')
    elif celula_selecionada['row'] == 3:
        df_bal_ativo = df_bal_ativo[['data', 'contas_a_receber']]
        fig = px.line(df_bal_ativo, x='data', y='contas_a_receber', title = ativo + ' - Contas a receber')
    elif celula_selecionada['row'] == 4:
        df_bal_ativo = df_bal_ativo[['data', 'estoque']]
        fig = px.line(df_bal_ativo, x='data', y='estoque', title = ativo + ' - Estoque')
    elif celula_selecionada['row'] == 5:
        df_bal_ativo = df_bal_ativo[['data', 'ativo_nao_circulante']]
        fig = px.line(df_bal_ativo, x='data', y='ativo_nao_circulante', title = ativo + ' - Ativo Não Circulante')
    elif celula_selecionada['row'] == 6:
        df_bal_ativo = df_bal_ativo[['data', 'investimentos']]
        fig = px.line(df_bal_ativo, x='data', y='investimentos', title = ativo + ' - Investimentos')
    elif celula_selecionada['row'] == 7:
        df_bal_ativo = df_bal_ativo[['data', 'imobilizado']]
        fig = px.line(df_bal_ativo, x='data', y='imobilizado', title = ativo + ' - Imobilizado')
    elif celula_selecionada['row'] == 8:
        df_bal_ativo = df_bal_ativo[['data', 'intangivel']]
        fig = px.line(df_bal_ativo, x='data', y='intangivel', title = ativo + ' - Intangível')
    elif celula_selecionada['row'] == 10:
        df_bal_ativo = df_bal_ativo[['data', 'passivo_circulante']]
        fig = px.line(df_bal_ativo, x='data', y='passivo_circulante', title = ativo + ' - Passivo Circulante')
    elif celula_selecionada['row'] == 11:
        df_bal_ativo = df_bal_ativo[['data', 'dividas_curto_prazo']]
        fig = px.line(df_bal_ativo, x='data', y='dividas_curto_prazo', title = ativo + ' - Dívidas de curto prazo')
    elif celula_selecionada['row'] == 12:
        df_bal_ativo = df_bal_ativo[['data', 'fornecedores']]
        fig = px.line(df_bal_ativo, x='data', y='fornecedores', title = ativo + ' - Fornecedores')
    elif celula_selecionada['row'] == 13:
        df_bal_ativo = df_bal_ativo[['data', 'passivo_nao_circulante']]
        fig = px.line(df_bal_ativo, x='data', y='passivo_nao_circulante', title = ativo + ' - Passivo Não Circulante')
    elif celula_selecionada['row'] == 14:
        df_bal_ativo = df_bal_ativo[['data', 'dividas_longo_prazo']]
        fig = px.line(df_bal_ativo, x='data', y='dividas_longo_prazo', title = ativo + ' - Dívidas de longo prazo')

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=350)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

"""
Ativo Circulante > Total Current Assets
    Aplicações financeiras > Short Term Investments
    Caixa > Cash
    Contas a receber > Net Receivables
    Estoque > Inventory
Ativo Não Circulante > Total Assets - Total Current Assets
    Investimentos > Long Term Investments
    Imobilizado > Property Plant Equipment
    Intangível > Intangible Assets

Passivo Circulante > Total Current Liabilities
    Dívidas de curto prazo > Short Long Term Debt
    Fornecedores > Accounts Payable
Passivo Não Circulante > Total Liab - Total Current Liabilities
    Dívidas de longo prazo > Long Term Debt
"""
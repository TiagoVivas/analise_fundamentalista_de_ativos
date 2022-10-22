from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

import pandas as pd

from app import app

dados = {
    ' ': ["Ativo Circulante",
          "  Aplicações financeiras",
          "  Caixa",
          "  Contas a receber",
          "  Estoque",
          "Ativo Não Circulante",
          "  Investimentos",
          "  Imobilizado",
          "  Intangível",
          "Passivo Circulante",
          "  Dívidas de curto prazo",
          "  Fornecedores",
          "Passivo Não Circulante",
          "  Dívidas de longo prazo"],
    'Data1': [i for i in range(14)],
    'Data2': [i for i in range(14)],
    'Data3': [i for i in range(14)],
    'Data4': [i for i in range(14)],
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
                                     id='balanco-tabela')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=7),
# Seção de gráficos -----------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='balanco-grafico')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=5)
    ])
])

# ============ Callbacks ============ #

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
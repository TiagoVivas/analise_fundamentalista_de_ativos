from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

import pandas as pd

from app import app

dados = {
    ' ': ["Receita total",
          "Custo dos produtos vendidos",
          "Despesas adm e vendas",
          "Pesquisa e desenvolvimento",
          "Despesas com juros",
          "Ebit",
          "Lucro bruto",
          "Lucro antes dos impostos",
          "Lucro líquido"],
    'Data1': [i for i in range(9)],
    'Data2': [i for i in range(9)],
    'Data3': [i for i in range(9)],
    'Data4': [i for i in range(9)],
}
df_financas = pd.DataFrame(dados)

# ============ Layout ============ #
layout = dbc.Col([
# Seção de filtros -------------------------------------------
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend("Filtro de finanças"),
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
                dash_table.DataTable(df_financas.to_dict('records'),
                                     [{'name': i, 'id': i} for i in df_financas.columns],
                                     id='financas-tabela')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=7),
# Seção de gráficos -----------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='financas-grafico')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=5)
    ])
])

# ============ Callbacks ============ #

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
"""
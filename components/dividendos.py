from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from datetime import datetime, timedelta
import plotly.express as px
from plotly.subplots import make_subplots

import yfinance as yf

from app import app
from globals import *

# ============ Layout ============ #
layout = dbc.Col([
    dbc.Card([
        dcc.Graph(id='dividendos_grafico')
    ], style={'height': '100%', 'padding': '10px'})
])

# ============ Callbacks ============ #
@app.callback(
    Output('dividendos_grafico', 'figure'),
    Input('store_ativo_selecionado', 'data')
)
def atualiza_grafico_dividendos(ativo):
    if (ativo is None) or (ativo == ''): # Pula primeira execução ao iniciar aplicação
        raise PreventUpdate

    lista_dividendos = []

    acao_yf = yf.Ticker(ativo + '.SA')
    df_dividendos = acao_yf.actions
    df_dividendos.reset_index(drop=False, inplace=True)
    df_dividendos.drop(columns='Stock Splits', inplace=True)
    df_dividendos = df_dividendos[df_dividendos['Dividends'] != 0]
    df_dividendos.Date = df_dividendos.Date.apply(lambda x: x.date())
    lista_de_datas_dividendos = df_dividendos.Date.to_list()

    lista_de_datas = [(datetime.today() - timedelta(days=x)).date() for x in range(3*365)]
    lista_de_datas.reverse()

    for data in lista_de_datas:
        if data not in lista_de_datas_dividendos:
            lista_dividendos.append(0)
        else:
            dividendo = df_dividendos[df_dividendos['Date'] == data]['Dividends'].sum()
            lista_dividendos.append(dividendo)

    dict_dados = {
        'Data': lista_de_datas,
        'Dividendos': lista_dividendos
    }
    df_dividendos = pd.DataFrame(dict_dados)

    fig = make_subplots()
    fig = px.bar(df_dividendos, x='Data', y='Dividendos')

    fig.update_traces(marker_color='rgb(0,255,0)', marker_line_color='rgb(0,255,0)', marker_line_width=5, opacity=1)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=500)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    for data in lista_de_datas:
        if (data.day == 1) & (data.month == 1):
            fig.add_vline(x=data, line_width=1, line_dash="dash", line_color="grey")

    return fig
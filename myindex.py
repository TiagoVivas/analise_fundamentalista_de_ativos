import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

from app import app
from components import infos, menu, cotacao, dividendos, financas, balanco, fluxo, indicadores, expectativas

# ============ Layout ============ #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'), 
            infos.layout
        ], md=3), # ocupa 2/12 da página
        dbc.Col([
            menu.layout,
            content
        ], md=9) # ocupa 10/12 da página
    ])
], fluid=True)

# ============ Callbacks ============ #
@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname')
)
def render_page(pathname):
    # Página Cotação
    if (pathname == '/') or (pathname == '/cotacao'):
        return cotacao.layout

    # Página de dividendos
    if pathname == '/dividendos':
        return dividendos.layout

    # Página de finanças
    if pathname == '/financas':
        return financas.layout

    # Página de balanço
    if pathname == '/balanco':
        return balanco.layout

    # Página de fluxo
    if pathname == '/fluxo':
        return fluxo.layout

    # Página de indicadores
    if pathname == '/indicadores':
        return indicadores.layout

    # Página de expectativas
    if pathname == '/expectativas':
        return expectativas.layout


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)


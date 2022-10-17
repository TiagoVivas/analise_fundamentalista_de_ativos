import dash_bootstrap_components as dbc

from app import app

# ============ Layout ============ #
layout = dbc.Row([
    dbc.Nav([
        dbc.NavLink("Cotação", href='/cotacao', active='exact'),
        dbc.NavLink("Dividendos", href='/dividendos', active='exact'),
        dbc.NavLink("Finanças", href='/financas', active='exact'),
        dbc.NavLink("Balanço", href='/balanco', active='exact'),
        dbc.NavLink("Fluxo", href='/fluxo', active='exact'),
        dbc.NavLink("Indicadores", href='/indicadores', active='exact'),
        dbc.NavLink("Expectativas", href='/expectativas', active='exact'),
    ], id='menu-navegacao', vertical=False, pills=True, style={'margin-left': '10px', 'margin-bottom': '10px'})
], id='menu-completo')

# ============ Callbacks ============ #
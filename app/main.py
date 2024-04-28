from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

import analysis
import explore
import discover
import home

nav = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Analyze", href="/analysis")),
                dbc.NavItem(dbc.NavLink("Explore", href="/explore")),
                dbc.NavItem(dbc.NavLink("Discover", href="/discover")),
            ] ,
            brand="Dinosaur World",
            brand_href="/",
            color="dark",
            dark=True,
            fixed="top",
        ), 
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analysis':
        return analysis.layout
    if pathname == '/explore':
        return explore.layout
    if pathname == "/discover":
        return discover.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app._favicon = "favico.ico"
app.title = "Dino-World"
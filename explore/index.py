from dash import dcc, html
from app import app
from explore import layout

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True, port=9000)
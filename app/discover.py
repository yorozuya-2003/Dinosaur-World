import dash
from dash import html
from app import app

layout = html.Div([
    html.Iframe(
        # style={"border": "1px solid rgba(0, 0, 0, 0.1)"},
        width="1440",
        height="5440",
        src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fproto%2FW1eyYLuWvEu1rJ3AhZImfs%2FDino-World%3Ftype%3Ddesign%26node-id%3D1-2%26t%3DKXPWrlIVyI2FtlvR-1%26scaling%3Dmin-zoom%26page-id%3D0%253A1%26mode%3Ddesign",
        style={'width':'100%'}
    )
], className= "discovery-frame")

if __name__ == '__main__':
    app.run_server(debug=True)

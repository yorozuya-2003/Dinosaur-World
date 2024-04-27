import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('data.csv')

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap']

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

# Define CSS styles
styles = {
    'main-container': {
        'display': 'flex',
        'font-family': 'Poppins, sans-serif',
    },
    'sidebar': {
        'background': '#11101d',
        'color': '#fff',
        'width': '260px',
        'padding': '20px',
        'font-family': 'Poppins, sans-serif',
        'position': 'fixed',  # Make sidebar fixed
        'height': '100vh',  # Make sidebar height 100% of the viewport
        'overflow-y': 'auto',  # Add vertical scrollbar if needed
    },
    'main-content': {
        'flex': '3',  # Take remaining space
        'padding': '30px',
        'background': '#f4f4f4',  # Change background color
        'color': '#333',  # Change font color
        'font-family': 'Poppins, sans-serif',
        'margin-left': '300px',  # Add margin to accommodate sidebar width
        'align': 'center',
    },
    'custom-dropdown': {
        'color': '#000',
        'margin-bottom': '15px',
        'margin-top': '10px',
    },
    'dropdown-label': {
        'margin-bottom': '5px',
    },
    'dino-details': {
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'space-between',
    },
}

# Define app layout
app.layout = html.Div([
    html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css", rel="stylesheet"),
    html.Div([
        html.H2('Dino Filters', style={'color': '#fff'}),
        html.Label('Name', style=styles['dropdown-label']),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df['name'].unique()],
            value=df['name'].unique()[0],
            className="custom-dropdown",
            style=styles['custom-dropdown'],
        ),
        html.Label('Diet', style=styles['dropdown-label']),
        dcc.Dropdown(
            id='diet-dropdown',
            options=[{'label': diet, 'value': diet} for diet in df['diet'].unique()],
            value=None,
            className="custom-dropdown",
            style=styles['custom-dropdown'],
        ),
        html.Label('Period (in million years ago)', style=styles['dropdown-label']),
        dcc.Dropdown(
            id='period-dropdown',
            options=[{'label': period[:len(period)-18], 'value': period} for period in df['period'].unique()],
            value=None,
            className="custom-dropdown",
            style=styles['custom-dropdown'],
        ),
        html.Label('Lived In', style=styles['dropdown-label']),
        dcc.Dropdown(
            id='live_in_dropdown',
            options=[{'label': place, 'value': place} for place in df['lived_in'].unique()],
            value=None,
            className="custom-dropdown",
            style=styles['custom-dropdown'],
        ),
        html.Label('Type', style=styles['dropdown-label']),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': type_, 'value': type_} for type_ in df['type'].unique()],
            value=None,
            className="custom-dropdown",
            style=styles['custom-dropdown'],
        ),
    ], style=styles['sidebar']),

    # Main section to display dinosaur info
    html.Div(id='main-content', style=styles['main-content'])
], style=styles['main-container'])

# Callback to update name dropdown options based on other filters
@app.callback(
    Output('name-dropdown', 'options', allow_duplicate=True),
    [Input('diet-dropdown', 'value'),
     Input('period-dropdown', 'value'),
     Input('live_in_dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_name_options(diet, period, place, type_):
    filtered_df = df
    
    if diet:
        filtered_df = filtered_df[filtered_df['diet'] == diet]
    if period:
        filtered_df = filtered_df[filtered_df['period'] == period]
    if place:
        filtered_df = filtered_df[filtered_df['lived_in'] == place]
    if type_:
        filtered_df = filtered_df[filtered_df['type'] == type_]
    return [{'label': name, 'value': name} for name in filtered_df['name'].unique()]

# # Callback to update dinosaur info based on filters
# @app.callback(
#     Output('main-content', 'children', allow_duplicate=True),
#     [Input('name-dropdown', 'value'),
#      Input('diet-dropdown', 'value'),
#      Input('period-dropdown', 'value'),
#      Input('live_in_dropdown', 'value'),
#      Input('type-dropdown', 'value')]
# )
# def update_dino_info(name, diet, period, place, type_):
#     dino = df[(df['diet'] == diet) | (df['period'] == period) | (df['lived_in'] == place) | (df['type'] == type_)]
#     if not dino.empty:
#         return html.Div([
#              html.Div([
#                 html.Div([
#                     html.H1(dino['name'].values[0].upper()),
#                     html.Img(src=dino['image'].values[0], alt='Image Description')
#                 ], style={'flex': '1'}),
#                 html.Div([
#                     html.P([html.I(className="fas fa-utensils"), f"  Diet: {dino['diet'].values[0]}"]),
#                     html.P([html.I(className="fas fa-clock"), f"  Period: {dino['period'].values[0]}"]),
#                     html.P([html.I(className="fas fa-globe"), f"  Lived in: {dino['lived_in'].values[0]}"]),
#                     html.P([html.I(className="fas fa-paw"), f"  Type: {dino['type'].values[0]}"]),
#                     html.P([html.I(className="fas fa-ruler"), f"  Length: {dino['length'].values[0]}m"]),
#                     html.P([html.I(className="fas fa-signature"), f"  Named by: {dino['named_by'].values[0]}"]),
#                 ], style={'flex': '1', 'margin-left': '20px', 'margin-top':'70px'}),
#             ], style=styles['dino-details']),
#             # Display world map below dinosaur image and information
#             dcc.Graph(id='world-map', figure=update_world_map(dino['lived_in'].values[0]))
#         ], style={'display': 'flex', 'flex-direction': 'column'})
#     else:
#         return html.P("No dinosaur found with selected criteria")

# Callback to update dinosaur info based on selected name
@app.callback(
    Output('main-content', 'children', allow_duplicate=True),
    [Input('name-dropdown', 'value')]
)
def update_dino_info_by_name(name):
    dino = df[df['name'] == name]
    if not dino.empty:
        return html.Div([
            html.Div([
                html.Div([
                    html.H1(dino['name'].values[0].upper()),
                    html.Img(src=dino['image'].values[0], alt='Image Description')
                ], style={'flex': '1'}),
                html.Div([
                    html.P([html.I(className="fas fa-utensils"), f"  Diet: {dino['diet'].values[0]}"]),
                    html.P([html.I(className="fas fa-clock"), f"  Period: {dino['period'].values[0]}"]),
                    html.P([html.I(className="fas fa-globe"), f"  Lived in: {dino['lived_in'].values[0]}"]),
                    html.P([html.I(className="fas fa-paw"), f"  Type: {dino['type'].values[0]}"]),
                    html.P([html.I(className="fas fa-ruler"), f"  Length: {dino['length'].values[0]}m"]),
                    html.P([html.I(className="fas fa-signature"), f"  Named by: {dino['named_by'].values[0]}"]),
                ], style={'flex': '1', 'margin-left': '20px', 'margin-top':'70px'}),
            ], style=styles['dino-details']),
            # Display world map below dinosaur image and information
            dcc.Graph(id='world-map', figure=update_world_map(dino['lived_in'].values[0]))
        ], style={'display': 'flex', 'flex-direction': 'column'})
    else:
        return html.P("No dinosaur found with selected criteria")

# Callback to update world map based on selected country
def update_world_map(lived_in):
    # Use plotly express to create a choropleth map
    fig = px.choropleth(locations=[lived_in], locationmode="country names", color_discrete_sequence=["blue"], title="Dinosaur Habitat")
    fig.update_layout(geo=dict(bgcolor='#f4f4f4'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

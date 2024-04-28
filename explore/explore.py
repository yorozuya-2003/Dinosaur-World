import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

from app import app

# load data
try:
    df = pd.read_csv('data_preprocessed.csv')
except:
    df = pd.read_csv('explore/data_preprocessed.csv')

# define app layout
layout = html.Div([
    html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css", rel="stylesheet"),
    html.Div([
        html.H2('Dino Filters', style={'color': '#fff'}),
        html.Label('Name', className='dropdown-label'),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df['name'].unique()],
            value=None,
            className="custom-dropdown",
        ),
        html.Hr(style={'border-color': '#ddd', 'margin-top': '10px', 'margin-bottom': '10px'}),
        html.Label('Diet', className='dropdown-label'),
        dcc.Dropdown(
            id='diet-dropdown',
            options=[{'label': diet, 'value': diet} for diet in df['diet'].unique()],
            value=None,
            className="custom-dropdown",
        ),
        html.Label('Period', className='dropdown-label'),
        dcc.Dropdown(
            id='period-dropdown',
            options=[{'label': period, 'value': period} for period in df['modified_period'].unique()],
            value=None,
            className="custom-dropdown",
        ),
        html.Label('Lived In', className='dropdown-label'),
        dcc.Dropdown(
            id='live_in_dropdown',
            options=[{'label': place, 'value': place} for place in df['lived_in'].unique()],
            value=None,
            className="custom-dropdown",
        ),
        html.Label('Type', className='dropdown-label'),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': type_, 'value': type_} for type_ in df['type'].unique()],
            value=None,
            className="custom-dropdown",
        ),
    ], className='sidebar'),

    # main section to display dinosaur info
    html.Div(id='main-content', className='main-content')
])


# callback to update name dropdown options based on other filters
@app.callback(
    Output('name-dropdown', 'options'),
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
        filtered_df = filtered_df[filtered_df['modified_period'] == period]
    if place:
        filtered_df = filtered_df[filtered_df['lived_in'] == place]
    if type_:
        filtered_df = filtered_df[filtered_df['type'] == type_]
    return [{'label': name, 'value': name} for name in filtered_df['name'].unique()]

# callback to update dinosaur cards based on selected name
@app.callback(
    Output('main-content', 'children'),
    [Input('name-dropdown', 'value')]
)
def update_dino_cards(name):
    if name is None:
        # if no name is selected, display cards for all dinosaurs
        return html.Div([
            html.H1('Dinosaur World', style={'margin-bottom': '20px', 'text-align':'center'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src=app.get_asset_url(f'images/{name}.jpg'), alt='Image Description', style={'width': '250%'}),
                        html.H4(name.upper()),
                    ], className='dino-card')
                ], style={'display': 'inline-block', 'margin-left': '3%', 'margin-right': '2%', 'width': '20%'}) for name in df['name']
            ])
        ])
    else:
        # if a name is selected, display the details of that dinosaur
        dino = df[df['name'] == name]
        if not dino.empty:
            return html.Div([
                html.Div([
                    html.Div([
                        html.H1(dino['name'].values[0].upper()),
                        html.Img(src=app.get_asset_url(f'images/{name}.jpg'), alt='Image Description')
                    ], style={'flex': '1'}),
                    html.Div([
                        html.P([html.I(className="fas fa-utensils"), f"  Diet: {dino['diet'].values[0]}"]),
                        html.P([html.I(className="fas fa-clock"), f"  Period: {dino['period'].values[0]}"]),
                        html.P([html.I(className="fas fa-globe"), f"  Lived in: {dino['lived_in'].values[0]}"]),
                        html.P([html.I(className="fas fa-paw"), f"  Type: {dino['type'].values[0]}"]),
                        html.P([html.I(className="fas fa-ruler"), f"  Length: {dino['length'].values[0]}m"]),
                        html.P([html.I(className="fas fa-signature"), f"  Named by: {dino['named_by'].values[0]}"]),
                    ], style={'flex': '1', 'margin-left': '20px', 'margin-top':'70px', 'font-size':'15px'}),
                ], className='dino-details'),
                # display world map below dinosaur image and information
                html.H2('Dinosaur Habitat'),
                dcc.Graph(id='world-map', figure=update_world_map(dino['lived_in'].values[0])),
            ], style={'display': 'flex', 'flex-direction': 'column'})
        else:
            return html.P("No dinosaur found with selected criteria")

# callback to update world map based on selected country
def update_world_map(lived_in):
    fig = px.choropleth(locations=[lived_in], locationmode="country names", color_discrete_sequence=["blue"], title="")
    fig.update_layout(geo=dict(bgcolor='#f4f4f4'))
    fig.update_layout(width=2000)
    fig.update_layout(showlegend=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

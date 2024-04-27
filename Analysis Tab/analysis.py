import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import country_converter as coco
cc = coco.CountryConverter()


def order_df(df_input, order_by, order):
    df_output=pd.DataFrame()
    for var in order:    
        df_append=df_input[df_input[order_by]==var].copy()
        df_output = pd.concat([df_output, df_append])
    return(df_output)

df = pd.read_csv('../data/dinosaurs_preprocessed.csv')
total_dinos = len(df)
total_dino_species = len(df.species.unique())
total_dino_types = len(df.type.unique())

country_counts = df['lived_in'].value_counts().reset_index()
country_counts['lived_in_iso'] = cc.pandas_convert(series=country_counts.lived_in, to='ISO3')


diet_order = ['Herbivorous', 'Carnivorous', 'Omnivorous', 'Unknown']
period_order = ['Late Triassic', 'Early Jurassic', 'Mid Jurassic', 'Late Jurassic', 'Early Cretaceous', 'Late Cretaceous']
type_order = ['Armoured Dinosaur', 'Ceratopsian', 'Euornithopod', 'Sauropod', 'Small Theropod', 'Large Theropod']

diet_df = order_df(df, 'diet', diet_order)
period_df = order_df(df, 'period', period_order)
type_df = order_df(df, 'type', type_order)

diet_counts = diet_df['diet'].value_counts()
period_counts = period_df['period'].value_counts()
type_counts = type_df['type'].value_counts()

ordered_df_dict = {
    'diet': diet_df,
    'period': period_df,
    'type': type_df
}

# species filtered dataframes
def filtered_df(filter_by, filter):
    df = ordered_df_dict[filter]
    temp = df.groupby([filter_by, filter]).size().unstack(fill_value=0).reset_index()
    temp['Total'] = temp.iloc[:, 1:].sum(axis=1)
    data = temp.sort_values(by='Total', ascending=False)
    data.drop('Total', axis=1, inplace=True)
    return data

app = dash.Dash(__name__)

app.layout = html.Div([
        html.H1('Dinosaur Data Analysis'),
        html.Div([
        html.Div([
            html.Div([
                html.Div("Total Dinosaurs",),
                html.H1(str(total_dinos), className='box')
            ], className='box'),

            html.Div([
                html.Div("Total Unique Species",),
                html.H1(str(total_dino_species), className='box')
            ], className='box'),

            html.Div([
                html.Div("Total Unique Types",),
                html.H1(str(total_dino_types), className='box')
            ], className='box')
        ], style={'display': 'flex', 'flexDirection': 'column'}),
        html.Div([
            dcc.Graph(id='diet-distribution'),
            html.Div("Diet Distribution"),
            dcc.Dropdown(
                id='diet-filter',
                options=[{'label': 'Diet: ' + diet, 'value': diet} for diet in diet_order],
                value=list(diet_order),
                multi=True,
                clearable=False
            ),
        ], className='box'),
        html.Div([
            html.Div(dcc.Graph(id='period-distribution')),
            html.Div("Period Distribution"),
            dcc.Dropdown(
                id='period-filter',
                options=[{'label': 'Period: ' + period, 'value': period} for period in period_order],
                value=list(period_order),
                multi=True,
                clearable=False
            ),
        ], className='box'),
        html.Div([
            dcc.Graph(id='type-distribution'),
            html.Div("Type Distribution"),
            dcc.Dropdown(
                id='type-filter',
                options=[{'label': 'Type: ' + type, 'value': type} for type in type_order],
                value=list(type_order),
                multi=True,
                clearable=False
            ),
        ], className='box')
    ], className='row'),
    html.Div([
        dcc.Graph(id='dinosaur-map', className='box'),
        html.Div([
            html.H3('Country-wise Distribution'),
            dcc.Graph(id='dinosaur-country', className='scrollable'),
            dcc.Dropdown(
                id='dinosaur-country-filter',
                options=[
                    {'label': 'Time Period', 'value': 'period'},
                    {'label': 'Diet', 'value': 'diet'},
                    {'label': 'Type', 'value': 'type'}
                ],
                value='period',
                clearable=False
            ),
        ], className='box'),
    ], className='row'),
    html.Div([
        html.Div([
            html.H3('Length-wise Distribution'),
            dcc.Graph(id='dinosaur-length', className='scrollable'),
            dcc.Dropdown(
                id='dinosaur-length-filter',
                options=[
                    {'label': 'Time Period', 'value': 'period'},
                    {'label': 'Diet', 'value': 'diet'},
                    {'label': 'Type', 'value': 'type'}
                ],
                value='period',
                clearable=False
            ),
        ], className='box'),
        html.Div([
            html.H3('Species-wise Distribution'),
            dcc.Graph(id='dinosaur-species', className='scrollable'),
            dcc.Dropdown(
                id='dinosaur-species-filter',
                options=[
                    {'label': 'Time Period', 'value': 'period'},
                    {'label': 'Diet', 'value': 'diet'},
                    {'label': 'Type', 'value': 'type'}
                ],
                value='period',
                clearable=False
            ),
        ], className='box'),
    ], className='row')
])


# Donut chart callbacks with filters
@app.callback(
    Output('diet-distribution', 'figure'),
    [Input('diet-filter', 'value')]
)
def update_diet_distribution(selected_diet):
    filtered_df = df[df['diet'].isin(selected_diet)]
    diet_counts = filtered_df['diet'].value_counts().reset_index()
    fig = px.pie(diet_counts,
                names='diet',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                )
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{label}</b>",
            "number of dinosaurs: %{value}",
        ])
    )
    return fig

@app.callback(
    Output('period-distribution', 'figure'),
    [Input('period-filter', 'value')]
)
def update_period_distribution(selected_period):
    filtered_df = df[df['period'].isin(selected_period)]
    period_counts = filtered_df['period'].value_counts().reset_index()
    fig = px.pie(period_counts,
                names='period',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                )
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{label}</b>",
            "number of dinosaurs: %{value}",
        ])
    )
    return fig

@app.callback(
    Output('type-distribution', 'figure'),
    [Input('type-filter', 'value')]
)
def update_type_distribution(selected_type):
    filtered_df = df[df['type'].isin(selected_type)]
    type_counts = filtered_df['type'].value_counts().reset_index()
    fig = px.pie(type_counts,
                names='type',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                )
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{label}</b>",
            "number of dinosaurs: %{value}",
        ])
    )
    return fig
# world map 
@app.callback(
    Output('dinosaur-map', 'figure'),
    [Input('dinosaur-map', 'hoverData')]
)
def update_map(hoverData):
    fig = px.choropleth(country_counts, locations="lived_in_iso",
            color="count",
            hover_name="lived_in",
            color_continuous_scale='agsunset_r',
            custom_data=['lived_in', 'count'],
            labels={'count': '# dinosaurs'})
    fig.update_layout(width=800, yaxis_title="# dinosaurs")
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "number of dinosaurs: %{customdata[1]}",
        ])
    )
    return fig

# dinosaurs length-wise chart
@app.callback(
    Output('dinosaur-length', 'figure'),
    [Input('dinosaur-length-filter', 'value')]
)
def update_dinosaur_lengths(filter_value):
    data = df.sort_values(by='length', ascending=False)
    fig = px.bar(data,
                 x='length', 
                 y='name', 
                 color=filter_value, 
                 orientation='h',
                 title='',
                 labels={'length': 'length (m)', 'name': 'dinosaur name', 'variable': ''})
    fig.update_layout(height=6000, width=800)
    fig.update_layout(yaxis=dict(autorange='reversed'))
    fig.update_layout(xaxis={'side': 'top'})
    fig.update_traces(
        hovertemplate="<br>".join([
            "name: <b>%{y}</b>",
            "length: %{x}m",
        ])
    )
    return fig
    return fig

# dinosaurs country-wise chart
@app.callback(
    Output('dinosaur-country', 'figure'),
    [Input('dinosaur-country-filter', 'value')]
)
def update_dinosaur_countries(filter_value):
    data = filtered_df('lived_in', filter_value)
    fig = px.bar(data, 
                 y='lived_in', 
                 x=data.columns[1:],
                 title = '',
                 orientation='h',
                 labels={'value': '# dinosaurs', 'lived_in': 'country', 'variable': ''})
    fig.update_layout(height=1000)
    fig.update_layout(yaxis=dict(autorange='reversed'))
    fig.update_layout(xaxis={'side': 'top'})
    fig.update_traces(
        hovertemplate="<br>".join([
            "country: <b>%{y}</b>",
            "number of dinosaurs: %{x}",
        ])
    )
    return fig

# dinosaurs species-wise chart
@app.callback(
    Output('dinosaur-species', 'figure'),
    [Input('dinosaur-species-filter', 'value')]
)
def update_dinosaur_species(filter_value):
    data = filtered_df('species', filter_value)
    fig = px.bar(data, 
                 y='species', 
                 x=data.columns[1:],
                 title = '',
                 orientation='h',
                 labels={'value': '# dinosaurs', 'species': 'dinosaur species','variable': ''})
    fig.update_layout(height=6000, width=800)
    fig.update_layout(yaxis=dict(autorange='reversed'))
    fig.update_layout(xaxis={'side': 'top'})
    fig.update_traces(
        hovertemplate="<br>".join([
            "species: <b>%{y}</b>",
            "number of dinosaurs: %{x}",
        ])
    )
    return fig

# main function
if __name__ == '__main__':
    app.run_server(debug=True, port=9000)

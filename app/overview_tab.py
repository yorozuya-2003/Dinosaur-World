from config import (
    app, px,
    dcc, html, Input, Output, 
    df, diet_order, country_counts, total_dinos, total_dino_species, total_dino_types,
    diet_order, period_order, type_order,
    filtered_df
)

overview_layout = html.Div([
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
            dcc.Graph(id='diet-distribution-donut'),
            html.Div("Diet Distribution"),
            dcc.Dropdown(
                id='diet-filter',
                options=[{'label': 'Diet: ' + each, 'value': each} for each in diet_order],
                value=list(diet_order),
                multi=True,
                clearable=False
            ),
        ], className='box'),

        html.Div([
            html.Div(dcc.Graph(id='period-distribution-donut')),
            html.Div("Period Distribution"),
            dcc.Dropdown(
                id='period-filter',
                options=[{'label': 'Period: ' + each, 'value': each} for each in period_order],
                value=list(period_order),
                multi=True,
                clearable=False
            ),
        ], className='box'),
        html.Div([
            dcc.Graph(id='type-distribution-donut'),
            html.Div("Type Distribution"),
            dcc.Dropdown(
                id='type-filter',
                options=[{'label': 'Type: ' + each, 'value': each} for each in type_order],
                value=list(type_order),
                multi=True,
                clearable=False
            ),
        ], className='box')
    ], className='row-box'),

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
    ], className='row-box'),

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
    ], className='row-box')
])


# donut charts with filters
@app.callback(
    Output('diet-distribution-donut', 'figure'),
    [Input('diet-filter', 'value')]
)
def update_diet_distribution_donut(selected_diet):
    filtered_df = df[df['diet'].isin(selected_diet)]
    diet_counts = filtered_df['diet'].value_counts().reset_index()
    diet_counts.columns = ['diet', 'count']
    fig = px.pie(diet_counts,
                names='diet',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                color_discrete_sequence=px.colors.qualitative.Prism,
                )
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{label}</b>",
            "number of dinosaurs: %{value}",
        ])
    )
    return fig

@app.callback(
    Output('period-distribution-donut', 'figure'),
    [Input('period-filter', 'value')]
)
def update_period_distribution_donut(selected_period):
    filtered_df = df[df['period'].isin(selected_period)]
    period_counts = filtered_df['period'].value_counts().reset_index()
    period_counts.columns = ['period', 'count']
    fig = px.pie(period_counts,
                names='period',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                color_discrete_sequence=px.colors.qualitative.Prism,
                )
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{label}</b>",
            "number of dinosaurs: %{value}",
        ])
    )
    return fig

@app.callback(
    Output('type-distribution-donut', 'figure'),
    [Input('type-filter', 'value')]
)
def update_type_distribution_donut(selected_type):
    filtered_df = df[df['type'].isin(selected_type)]
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.pie(type_counts,
                names='type',
                values='count', 
                title='', hole=0.3, width=450, height=300,
                color_discrete_sequence=px.colors.qualitative.Prism,
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
            labels={'count': 'number of dinosaurs'})
    fig.update_layout(width=800, yaxis_title="number of dinosaurs")
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
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 labels={'length': 'length (m)', 'name': 'dinosaur name', 'variable': '', filter_value:''})
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
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 labels={'value': 'number of dinosaurs', 'lived_in': 'country', 'variable': ''})
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
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 labels={'value': 'number of dinosaurs', 'species': 'dinosaur species','variable': ''})
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
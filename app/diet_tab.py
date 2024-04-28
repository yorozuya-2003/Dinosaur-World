from config import (
    app, px,
    dcc, html, Input, Output, 
    df, diet_order,
    filter_world_counts, analysis_plot_figure
)

diet_layout = html.Div([
        html.Div([
            dcc.Graph(id='diet-distribution-bar', className='box'),
        html.Div([
            dcc.Dropdown(
                id='diet-map-filter',
                options=[
                    {'label': each, 'value': each} for each in diet_order],
                value=diet_order[0],
                clearable=False
            ),
            dcc.Graph(id='diet-map', className='scrollable'),
        ], className='box'),
        ], className='row-box'),

        html.Div([html.Div([
                html.H3('Period-wise Distribution'),
                dcc.Graph(id='diet-analysis-period', className='scrollable'),
            ], className='box'),
            html.Div([
                html.H3('Type-wise Distribution'),
                dcc.Graph(id='diet-analysis-type', className='scrollable'),
            ], className='box'),
        ], className='row-box'),
    ])


# bar chart
@app.callback(
    Output('diet-distribution-bar', 'figure'),
    [Input('diet-distribution-bar', 'hoverData')]
)
def update_diet_distribution_bar(hoverData):
    diet_counts = df['diet'].value_counts().reset_index()
    diet_counts.columns = ['diet', 'count']
    fig = px.bar(diet_counts,
                x='diet',
                y='count',
                title='',
                color='diet',
                labels={'diet': 'Diet', 'count': 'number of dinosaurs'},
                color_discrete_sequence=px.colors.qualitative.Prism
                )
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_title='', yaxis_title='number of dinosaurs')
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{x}</b>",
            "number of dinosaurs: %{y}",
        ])
    )
    return fig

# world map 
@app.callback(
    Output('diet-map', 'figure'),
    [Input('diet-map-filter', 'value')]
)
def update_diet_map(filter_value):
    data = filter_world_counts('diet', filter_value)
    fig = px.choropleth(data, locations="lived_in_iso",
            color="count",
            hover_name="lived_in",
            color_continuous_scale='Tealgrn',
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

# diet analysis charts
@app.callback(
    Output('diet-analysis-period', 'figure'),
    [Input('diet-analysis-period', 'hoverData')]
)
def update_diet_anlysis_period(hoverData):
    fig = analysis_plot_figure('diet', 'period')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output('diet-analysis-type', 'figure'),
    [Input('diet-analysis-type', 'hoverData')]
)
def update_diet_anlysis_type(hoverData):
    fig = analysis_plot_figure('diet', 'type')
    fig.update_layout(height=400)
    return fig
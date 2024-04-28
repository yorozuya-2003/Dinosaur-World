from config import (
    app, px,
    dcc, html, Input, Output, 
    df, period_order,
    filter_world_counts, analysis_plot_figure
)

period_layout = html.Div([
        html.Div([
            dcc.Graph(id='period-distribution-bar', className='box'),
        html.Div([
            dcc.Dropdown(
                id='period-map-filter',
                options=[
                    {'label': each, 'value': each} for each in period_order],
                value=period_order[0],
                clearable=False
            ),
            dcc.Graph(id='period-map', className='scrollable'),
        ], className='box'),
        ], className='row-box'),

        html.Div([html.Div([
                html.H3('Type-wise Distribution'),
                dcc.Graph(id='period-analysis-type', className='scrollable'),
            ], className='box'),
            html.Div([
                html.H3('Diet-wise Distribution'),
                dcc.Graph(id='period-analysis-diet', className='scrollable'),
            ], className='box'),
        ], className='row-box'),
    ])


# bar chart
@app.callback(
    Output('period-distribution-bar', 'figure'),
    [Input('period-distribution-bar', 'hoverData')]
)
def update_period_distribution_bar(hoverData):
    period_counts = df['period'].value_counts().reset_index()
    period_counts.columns = ['period', 'count']
    fig = px.bar(period_counts,
                x='period',
                y='count',
                title='',
                color='period',
                labels={'period': 'Period', 'count': 'number of dinosaurs'},
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
    Output('period-map', 'figure'),
    [Input('period-map-filter', 'value')]
)
def update_period_map(filter_value):
    data = filter_world_counts('period', filter_value)
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

# period analysis charts
@app.callback(
    Output('period-analysis-type', 'figure'),
    [Input('period-analysis-type', 'hoverData')]
)
def update_period_anlysis_type(hoverData):
    fig = analysis_plot_figure('period', 'type')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output('period-analysis-diet', 'figure'),
    [Input('period-analysis-diet', 'hoverData')]
)
def update_period_anlysis_diet(hoverData):
    fig = analysis_plot_figure('period', 'diet')
    fig.update_layout(height=400)
    return fig
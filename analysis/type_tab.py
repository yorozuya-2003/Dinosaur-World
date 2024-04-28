from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

try:
    from config import (
        df, type_order,
        filter_world_counts, analysis_plot_figure
    )
except:
    from analysis.config import (
        df, type_order,
        filter_world_counts, analysis_plot_figure
    )
from app import app

type_layout = html.Div([
        html.Div([
            dcc.Graph(id='type-distribution-bar', className='box'),
        html.Div([
            dcc.Dropdown(
                id='type-map-filter',
                options=[
                    {'label': each, 'value': each} for each in type_order],
                value=type_order[0],
                clearable=False
            ),
            dcc.Graph(id='type-map', className='scrollable'),
        ], className='box'),
        ], className='row'),

        html.Div([html.Div([
                html.H3('Period-wise Distribution'),
                dcc.Graph(id='type-analysis-period', className='scrollable'),
            ], className='box'),
            html.Div([
                html.H3('Diet-wise Distribution'),
                dcc.Graph(id='type-analysis-diet', className='scrollable'),
            ], className='box'),
        ], className='row'),
    ])


# bar chart
@app.callback(
    Output('type-distribution-bar', 'figure'),
    [Input('type-distribution-bar', 'hoverData')]
)
def update_type_distribution_bar(hoverData):
    type_counts = df['type'].value_counts().reset_index()
    fig = px.bar(type_counts,
                x='type',
                y='count',
                title='',
                color='type',
                labels={'type': 'Type', 'count': 'number of dinosaurs'},
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
    Output('type-map', 'figure'),
    [Input('type-map-filter', 'value')]
)
def update_type_map(filter_value):
    data = filter_world_counts('type', filter_value)
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

# type analysis charts
@app.callback(
    Output('type-analysis-period', 'figure'),
    [Input('type-analysis-period', 'hoverData')]
)
def update_type_anlysis_period(hoverData):
    fig = analysis_plot_figure('type', 'period')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output('type-analysis-diet', 'figure'),
    [Input('type-analysis-diet', 'hoverData')]
)
def update_type_anlysis_diet(hoverData):
    fig = analysis_plot_figure('type', 'diet')
    fig.update_layout(height=400)
    return fig
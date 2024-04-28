from config import (
    app,
    html, dcc, Input, Output,
)
from overview_tab import overview_layout
from diet_tab import diet_layout
from period_tab import period_layout
from type_tab import type_layout

layout = html.Div([
    # html.H2('Dinosaur Data Analysis', style={'margin-top':'10px'}),
    dcc.Tabs(id='tabs', value='tab-overview', children=[
        dcc.Tab(label='Overview', value='tab-overview'),
        dcc.Tab(label='Period Analysis', value='tab-period'),
        dcc.Tab(label='Type Analysis', value='tab-type'),
        dcc.Tab(label='Diet Analysis', value='tab-diet'),
    ]),
    html.Div(id='tabs-content')
])

# render tabs
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-overview':
        return overview_layout
    elif tab == 'tab-period':
        return period_layout
    elif tab == 'tab-type':
        return type_layout
    elif tab == 'tab-diet':
        return diet_layout
    else:
        return html.Div('Error: Invalid tab selected')

# main function
if __name__ == '__main__':
    app.run_server(debug=True, port=9000)

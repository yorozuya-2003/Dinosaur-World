from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from netCDF4 import Dataset
import numpy as np

import pandas as pd
dinosaur_data = pd.read_csv('analysis_data.csv')

from app import app

WIDTH = 900
HEIGHT = 800

def Etopo(lon_area, lat_area, resolution):
    data = Dataset("ETOPO1_Ice_g_gdal.grd", "r")
    lon_range = data.variables['x_range'][:]
    lat_range = data.variables['y_range'][:]
    topo_range = data.variables['z_range'][:]
    spacing = data.variables['spacing'][:]
    dimension = data.variables['dimension'][:]
    z = data.variables['z'][:]
    lon_num = dimension[0]
    lat_num = dimension[1]
  
    lon_input = np.zeros(lon_num); lat_input = np.zeros(lat_num)
    for i in range(lon_num):
        lon_input[i] = lon_range[0] + i * spacing[0]
    for i in range(lat_num):
        lat_input[i] = lat_range[0] + i * spacing[1]

    lon, lat = np.meshgrid(lon_input, lat_input)
    topo = np.reshape(z, (lat_num, lon_num))

    if ((resolution < spacing[0]) | (resolution < spacing[1])):
        print('Set the highest resolution')
    else:
        skip = int(resolution/spacing[0])
        lon = lon[::skip,::skip]
        lat = lat[::skip,::skip]
        topo = topo[::skip,::skip]
    
    topo = topo[::-1]

    range1 = np.where((lon>=lon_area[0]) & (lon<=lon_area[1]))
    lon = lon[range1]; lat = lat[range1]; topo = topo[range1]
    range2 = np.where((lat>=lat_area[0]) & (lat<=lat_area[1]))
    lon = lon[range2]; lat = lat[range2]; topo = topo[range2]
    lon_num = len(np.unique(lon))
    lat_num = len(np.unique(lat))
    lon = np.reshape(lon, (lat_num, lon_num))
    lat = np.reshape(lat, (lat_num, lon_num))
    topo = np.reshape(topo, (lat_num, lon_num))

    return lon, lat, topo

def degree2radians(degree):
    return degree*np.pi/180
  
def mapping_map_to_sphere(lon, lat, radius=1):
    lon=np.array(lon, dtype=np.float64)
    lat=np.array(lat, dtype=np.float64)
    lon=degree2radians(lon)
    lat=degree2radians(lat)
    xs=radius*np.cos(lon)*np.cos(lat)
    ys=radius*np.sin(lon)*np.cos(lat)
    zs=radius*np.sin(lat)
    return xs, ys, zs


resolution = 0.8
lon_area = [-180., 180.]
lat_area = [-90., 90.]

lon_topo, lat_topo, topo = Etopo(lon_area, lat_area, resolution)
xs, ys, zs = mapping_map_to_sphere(lon_topo, lat_topo)
Ctopo = [[0, 'rgb(0, 0, 70)'],[0.2, 'rgb(0,90,150)'], 
          [0.4, 'rgb(150,180,230)'], [0.5, 'rgb(210,230,250)'],
          [0.50001, 'rgb(0,120,0)'], [0.57, 'rgb(220,180,130)'], 
          [0.65, 'rgb(120,100,0)'], [0.75, 'rgb(80,70,0)'], 
          [0.9, 'rgb(200,200,200)'], [1.0, 'rgb(255,255,255)']]
cmin = -8000
cmax = 8000

topo_sphere=dict(type='surface',
  x=xs,
  y=ys,
  z=zs,
  colorscale=Ctopo,
  surfacecolor=topo,
  showscale=False,
  cmin=cmin,
  cmax=cmax)
noaxis=dict(showbackground=False,
  showgrid=False,
  showline=False,
  showticklabels=False,
  ticks='',
  title='',
  zeroline=False)

titlecolor = 'white'
bgcolor = 'dimgray'

def add_marker(lat, long, name):
    xs, ys, zs = mapping_map_to_sphere(long, lat)
    marker_trace = go.Scatter3d(
        x=[xs],
        y=[ys],
        z=[zs],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='circle'
        ),
        name=name,
    )
    return marker_trace

dropdown_options = [{'label': row['name'], 'value': idx} for idx, row in dinosaur_data.iterrows()]
plot_data=[topo_sphere]


layout = html.Div(children=[
    html.Div([
        html.H4("Locate dinosaur habitats around the globe!"),
        dcc.Dropdown(
            id='dinosaur-dropdown',
            options=dropdown_options,
            value=0,
            style={'width':'80%', 'font-size':'20px'}
        ),
    ], className='box', style={'height': '100vh', 'display':'flex', 'flex-direction':'column',
                               'justify-content':'center', 'align-items':'center',}),
    dcc.Graph(
        id='earth-visualization',
        figure={
            'data': plot_data,
            'layout': go.Layout(
                title='',
                autosize=False,
                width=WIDTH,
                height=HEIGHT,
                showlegend=False,
                scene=dict(
                    xaxis=dict(showgrid=False, visible=False),
                    yaxis=dict(showgrid=False, visible=False),
                    zaxis=dict(showgrid=False, visible=False),
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=1),
                ),
                paper_bgcolor='black',
                plot_bgcolor='white'
            )
        }, 
        style={'height': '100vh', 'background-color':'black'},
    ),
], className='row-box')


@app.callback(
    Output('earth-visualization', 'figure'),
    [Input('dinosaur-dropdown', 'value')]
)
def update_plot(selected_dinosaur_index):
    selected_dinosaur = dinosaur_data.iloc[selected_dinosaur_index]
    lat = selected_dinosaur['latitude']
    long = selected_dinosaur['longitude']
    marker_trace = add_marker(lat, long, selected_dinosaur['name'])
    updated_plot_data = plot_data + [marker_trace]
    updated_figure = {
        'data': updated_plot_data,
        'layout': go.Layout(
            title='',
            autosize=False,
            width=WIDTH,
            height=HEIGHT,
            showlegend=False,
            scene=dict(
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, visible=False),
                zaxis=dict(showgrid=False, visible=False),
                aspectmode='manual',
                aspectratio=dict(x=1, y=1, z=1),
            ),
            paper_bgcolor='black',
            plot_bgcolor='white'
        )
    }
    
    return updated_figure

if __name__ == '__main__':
    app.run_server(debug=True)

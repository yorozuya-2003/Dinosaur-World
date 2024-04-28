import json
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# import country_converter as coco
# cc = coco.CountryConverter()

def order_df(df_input, order_by, order):
    df_output=pd.DataFrame()
    for var in order:    
        df_append=df_input[df_input[order_by]==var].copy()
        df_output = pd.concat([df_output, df_append])
    return(df_output)

try:
    df = pd.read_csv('data_preprocessed.csv')
except:
    df = pd.read_csv('analysis/data_preprocessed.csv')

total_dinos = len(df)
total_dino_species = len(df.species.unique())
total_dino_types = len(df.type.unique())

try:
    with open('iso_mapping.json', 'r') as openfile:
        iso_mapping = json.load(openfile)
except:
    with open('analysis/iso_mapping.json', 'r') as openfile:
        iso_mapping = json.load(openfile)

country_counts = df['lived_in'].value_counts().reset_index()
country_counts['lived_in_iso'] = country_counts.lived_in.map(iso_mapping)
# country_counts['lived_in_iso'] = cc.pandas_convert(series=country_counts.lived_in, to='ISO3')
# country_counts.to_csv('country_counts.csv', index=False)
# country_counts = pd.read_csv('country_counts.csv')
# iso_mapping = {}
# for each in range(len(country_counts)):
#     iso_mapping[country_counts.iloc[each].lived_in] = country_counts.iloc[each].lived_in_iso

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

# filtered dataframes
def filtered_df(filter_by, filter):
    df = ordered_df_dict[filter]
    temp = df.groupby([filter_by, filter]).size().unstack(fill_value=0).reset_index()
    temp['Total'] = temp.iloc[:, 1:].sum(axis=1)
    data = temp.sort_values(by='Total', ascending=False)
    data.drop('Total', axis=1, inplace=True)
    return data

# analysis plot
def analysis_plot_figure(filter_by, filter):
    data = filtered_df(filter_by, filter)
    fig = px.bar(data, 
                y=filter_by, 
                x=data.columns[1:],
                title = '',
                orientation='h',
                color_discrete_sequence=px.colors.qualitative.Prism,
                labels={'value': '# dinosaurs', filter_by: filter_by, 'variable': ''})
    fig.update_layout(yaxis=dict(autorange='reversed'))
    fig.update_layout(xaxis={'side': 'top'})
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{y}</b>",
            "number of dinosaurs: %{x}",
        ])
    )
    return fig

# filtered data for map
def filter_world_counts(column, value):
    data = df[df[column]==value]
    data = data['lived_in'].value_counts().reset_index()
    data['lived_in_iso'] = data.lived_in.map(iso_mapping)
    return data

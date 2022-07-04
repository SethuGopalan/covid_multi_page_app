from numpy import equal, isin
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from dash import Dash, html, dcc
import dash
from dash import Input, Output, dash_table, callback
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page

register_page(__name__)
df = pd.read_csv('app_folder\Worldwide country-level data.csv')
dff = df.dropna(axis=1, thresh=2)
data1 = dff['iso_alpha_3']
data2 = data1.dropna()
data3 = dff['deaths']
data4 = data3.dropna()

data5 = df[['iso_alpha_3', "date", "confirmed",
            "deaths", "recovered"]].drop_duplicates()
data6 = data5.dropna()

layout = dbc.Container([

    dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="my_dropdown",style={'color': 'black'},
                    options=[{'label': i, 'value': i}
                             for i in data2.unique()],
                    value=["USA"],
                    multi=True,),
            ], width={'size': 5, 'offset': 0}),
            dbc.Col([

                dcc.Graph(id="graph3"),
            ], width={'size': 12, 'offset': 0}),

            ], justify='center'),

])

@callback(Output("graph3", "figure"), Input("my_dropdown", "value"))
def filter_scatter(country):
    dff = df[df['iso_alpha_3'].isin(country)]
    fig3 = px.scatter(dff, x='date', y='deaths', color="iso_alpha_3",  size_max=65,
                      hover_name='iso_alpha_3', hover_data=['deaths', 'date', 'confirmed', 'recovered'])
    return fig3

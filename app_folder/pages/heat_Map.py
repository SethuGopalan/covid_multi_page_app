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
                        id="my_dropdown", style={"border": "2px black solid"},
                        options=[{'label': i, 'value': i}
                                 for i in data2.unique()],

                        value=["USA"],
                        multi=True,),

                    ], width={'size': 5, 'offset': 0}, style={"border": "2px black solid"}),



            dbc.Col([

                dcc.Graph(id="graph2"),
            ], width={'size': 12, 'offset': 0}, style={"border": "2px black solid"}),

            ], justify='center'),


])


@callback(Output("graph2", "figure"), Input("my_dropdown", "value"))
def filter_scatter(country):
    dff = df[df['iso_alpha_3'].isin(country)]
    fig = px.imshow(dff, labels=dict(
        x='{} is selected'.format(str(country)[1:-1]), y='{} Covid data range'.format(str(country)[1:-1])))
    return fig

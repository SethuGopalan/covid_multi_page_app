from numpy import equal, isin
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from dash import Dash, html, dcc
import dash
from dash import Input, Output, dash_table
import numpy as np
import pandas as pd

from dash_labs.plugins.pages import register_page


import dash_bootstrap_components as dbc

# data section
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
                dash_table.DataTable(
                    data=data6.to_dict('records'),
                    columns=[{"id": i, "name": i, }
                             for i in data6.columns

                             ],
                    fixed_rows={'headers': True},
                    style_table={'maxhight': '120px', 'maxwidth': 15},
                    page_size=100,
                    style_header={
                        'font_family': 'cursive',
                        'font_size': '10px',
                        'font_Color': 'white',
                        'backgroundColor': 'green',
                        'text_align': 'center',
                        'border': '4px solid white', },
                    style_data_conditional=[
                        {'if': {'column_id': 'iso_alpha_3'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'date'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'confirmed'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'recovered'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'deaths'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                    ],
                    style_cell={
                        'textAlign': 'center'
                    },


                ),
            ], width={'size': 14, 'offset': 0}),

            ])

])

from numpy import equal, isin
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from dash import Dash, html, dcc
import dash
from dash import Input, Output, dash_table
import numpy as np
import pandas as pd
import requests
from tabulate import tabulate

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

# ''' live data for today continental '''

url = 'https://disease.sh/v3/covid-19/continents'
r = requests.get(url)
data = r.json()
# ''' live data for todays country'''

new_data = pd.DataFrame(data)

newCont_data = new_data[['continent',  'cases', 'todayCases', 'deaths',
                         'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]
newdataCT = newCont_data.groupby('continent').agg({'todayDeaths': [max, min]})
# new_max = newCont_data.nlargest(
#     1, ['todayDeaths', 'todayCases']).loc[:'continent']
row_of_max_index = newCont_data.loc[newCont_data['todayDeaths'].idxmax(
)].to_string()
row_of_min_index = newCont_data.loc[newCont_data['todayDeaths'].idxmin(
)].to_string()
# new_max = newCont_data.max()['todayDeaths']
# new_data = new_data.reset_index(drop=True)
# dff_data = new_data[['continent', 'countries']]
# Tdata = new_data.set_index('country', inplace=True),
# newTdata = new_data.drop(columns='continent')
# newTdata = Tdata.set_index(['country'])

url = 'https://disease.sh/v3/covid-19/countries'
r = requests.get(url)
con_data = r.json()


newCon_data = pd.DataFrame(con_data)
# TBdata = newCon_data.dropna()
newdata = newCon_data.groupby('country').agg({'todayDeaths': [max, min]})
newTBdata = newCon_data[['country',  'cases', 'todayCases', 'deaths',
                         'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]
row_of_max = newTBdata.loc[newTBdata['todayDeaths'].idxmax()].to_string()
row_of_min = newTBdata.loc[newTBdata['todayDeaths'].idxmin()].to_string()
# TBdata = newTBdata


layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5('Covid Data latest Every Country ')
            ],   style={'color': 'white',  'fontSize': 5, 'font-family': 'serif'}),
        ], width={'size': 3, 'offset': 0},),
        dbc.Col([
            html.Div([
                html.H5('Covid Data latest Every Continent ')
            ],   style={'color': 'white',  'fontSize': 5, 'font-family': 'serif'}),
        ], width={'size': 4, 'offset': 4},),
    ], style={'border': "1px gray double", }),
    html.Br(),
    html.Br(),
    dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    data=newTBdata.to_dict('records'),
                    columns=[{"id": i, "name": i, }
                             for i in newTBdata.columns

                             ],
                    fixed_rows={'headers': True},
                    style_table={'maxhight': '120px',
                                 'maxwidth': '100%', 'minWidth': '100%'},
                    page_size=6,

                    style_header={
                        'font_family': 'serif',
                        'font_size': '10px',
                        'font_Color': 'white',
                        'backgroundColor': 'black',
                        'maxWidth': '100%',
                        'text_align': 'center',
                        'border': '4px solid black', },
                    style_data_conditional=[
                        {'if': {'column_id': 'country'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         }, {'if': {'column_id': 'updated'},
                             'backgroundColor': 'white',
                             'color': 'black',
                             },
                        {'if': {'column_id': 'cases'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayCases'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'deaths'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayDeaths'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'recovered'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayRecovered'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'active'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'critical'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },

                    ],
                    style_cell={
                        'textAlign': 'center'
                    },


                ),
            ], width={'size': 6, 'offset': 0}, style={"border": "1px gray double"}),
            dbc.Col([
                dash_table.DataTable(
                    data=newCont_data.to_dict('records'),
                    columns=[{"id": i, "name": i, }
                             for i in newCont_data.columns

                             ],
                    fixed_rows={'headers': True},
                    style_table={'maxhight': '10px',
                                 'maxwidth': '100%', 'minWidth': '100%'},
                    page_size=10,

                    style_header={
                        'font_family': 'serif',
                        'font_size': '10px',
                        'font_Color': 'white',
                        'backgroundColor': 'black',
                        'maxWidth': '100%',
                        'text_align': 'center',
                        'border': '4px solid black', },
                    style_data_conditional=[
                        {'if': {'column_id': 'continent'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         }, {'if': {'column_id': 'updated'},
                             'backgroundColor': 'white',
                             'color': 'black',
                             },
                        {'if': {'column_id': 'cases'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayCases'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'deaths'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayDeaths'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'recovered'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'todayRecovered'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'active'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },
                        {'if': {'column_id': 'critical'},
                         'backgroundColor': 'white',
                         'color': 'black',
                         },

                    ],
                    style_cell={
                        'textAlign': 'center'
                    },


                ),
            ], width={'size': 6, 'offset': 0}, style={"border": "1px gray double"})


            ]),
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([

            html.Div([

                (f"'Todays highest Death: {row_of_max}")

            ]),

        ], width={'size': 3, 'offset': 0}, style={"border": "1px gray double"}),

        dbc.Col([

            html.Div([

                (f"'Todays highest Death: {row_of_max_index}")

            ]),

        ], width={'size': 3, 'offset': 6}, style={"border": "1px gray double"}),


    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([

            html.Div([

                (f"'Todays Lowest Death: {row_of_min}")

            ]),

        ], width={'size': 3, 'offset': 0}, style={"border": "1px gray double"}),

        dbc.Col([

            html.Div([

                (f"'Todays Lowest Death: {row_of_min_index}")

            ]),

        ], width={'size': 3, 'offset': 6}, style={"border": "1px gray double"}),


    ]),


], style={"border": "1px gray double double"}),

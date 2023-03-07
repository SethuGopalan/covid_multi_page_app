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
import requests
from dash_bootstrap_templates import load_figure_template
load_figure_template("sketchy")
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

url = 'https://disease.sh/v3/covid-19/continents'
r = requests.get(url)
data = r.json()
# ''' live data for todays country'''

new_data = pd.DataFrame(data)

newCont_data = new_data[['continent',  'cases', 'todayCases', 'deaths',
                         'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]
Rd_data = new_data[['cases', 'todayCases', 'deaths',
                    'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]

newdataCT = newCont_data.groupby('continent').agg({'todayDeaths': [max, min]})

row_of_max_index = newCont_data.loc[newCont_data['todayDeaths'].idxmax(
)].to_string()
row_of_min_index = newCont_data.loc[newCont_data['todayDeaths'].idxmin(
)].to_string()


url = 'https://disease.sh/v3/covid-19/countries'
r = requests.get(url)
con_data = r.json()


newCon_data = pd.DataFrame(con_data)
# TBdata = newCon_data.dropna()
newdata = newCon_data.groupby('country').agg({'todayDeaths': [max, min]})
newTBdata = newCon_data[['country',  'cases', 'todayCases', 'deaths',
                         'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]
Lg_color = newCon_data[['cases', 'todayCases', 'deaths',
                        'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical']]

row_of_max = newTBdata.loc[newTBdata['todayDeaths'].idxmax()].to_string()
row_of_min = newTBdata.loc[newTBdata['todayDeaths'].idxmin()].to_string()

layout = dbc.Container([

    dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="x_dropdown", style={'color': 'black'},
                    options=[{'label': x, 'value': x}
                             for x in newTBdata.columns],
                    value="deaths",
                ),
            ], width={'size': 5, 'offset': 0}),
            dbc.Col([
                dcc.Dropdown(
                    id="y_dropdown", style={'color': 'black'},
                    options=[{'label': y, 'value': y}
                             for y in newTBdata.columns],
                    value="todayDeaths",
                ),
            ], width={'size': 5, 'offset': 0}, style={"border": "2px black solid"}),
            dbc.Col([

                dcc.Graph(id="graph3"),
            ], width={'size': 12, 'offset': 0}),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Col([
            html.Br(),
                dcc.Graph(id="graph4"),
            ], width={'size': 12, 'offset': 0}, style={"border": "2px black solid"}),

            ], justify='center'),
])


@callback(Output("graph3", "figure"),
          Output("graph4", "figure"),
          Input("x_dropdown", "value"),
          Input("y_dropdown", "value"))
def filter_scatter(x_value, y_value):
    # dff = newTBdata[newTBdata['country'].isin(country)]
    fig3 = px.scatter(newTBdata, x=x_value, y=y_value, color=newTBdata['country'], size=y_value, size_max=50,
                      hover_name=newTBdata['country'], )
    fig = px.scatter(newCont_data, x=newCont_data['deaths'], y=newCont_data['todayDeaths'],
                     facet_col='continent', color=newCont_data['todayDeaths'], size='deaths', size_max=50)
    return fig3, fig

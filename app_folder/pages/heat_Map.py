from matplotlib.pyplot import colorbar
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
                        id="my_dropdown", style={"border": "2px black solid"},
                        options=[{'label': i, 'value': i}
                                 for i in newTBdata['country']],

                        value="USA",
                    ),

                    ], width={'size': 2, 'offset': 0}, style={"border": "2px black solid"}),
            dbc.Col([
                    dcc.Dropdown(
                        id="item_dropdown", style={"border": "2px black solid"},
                        options=[{'label': p, 'value': p}
                                 for p in Lg_color],

                        value="todayCases",
                    ),

                    ], width={'size': 2, 'offset': 0}, style={"border": "2px black solid"}),

            dbc.Col([

                dcc.Graph(id="graph2"),
            ], width={'size': 10, 'offset': 0}, style={"border": "2px black solid"}),

            ], justify='center'),
    dbc.Row([

        dbc.Col([

            dcc.RadioItems(id="cont_dropdown",
                           options=[{'label': r, 'value': r}
                                    for r in Rd_data.columns],
                           value='todayCases',
                           ),
        ], width={'size': 2, 'offset': 0}, style={"border": "2px black solid"}),

        dbc.Col([
                dcc.Graph(id="sp_graph")
                ], width={'size': 8, 'offset': 0}, style={"border": "2px black solid"}),
    ], justify='center')




],style={"border": "2px black solid"})


@ callback(Output("graph2", "figure"),
           Output("sp_graph", "figure"),
           Input("my_dropdown", "value"),
           Input("item_dropdown", "value"),
           Input("cont_dropdown", "value"))
def filter_scatter(update_country, item_update, Cont_update):
    dff = newTBdata[newTBdata['country'] == update_country]
    data_c = dff.drop(columns=dff.columns[0])
    # dff_cont = Rd_data[Rd_data.columns.isin(Cont_update)]

    fig = px.imshow(data_c, labels=dict(color=item_update, hover_data=['cases', 'todayCases', 'deaths',
                                                                       'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical'],

                                        x='{} is selected'.format(str(update_country)), y='{} Covid data range'.format(str(update_country))))

    fig.update_layout(plot_bgcolor="gray",
                      paper_bgcolor="gray")
    fig2 = px.box(
        Rd_data, x=newCont_data['continent'], y=Cont_update, points="all",
        boxmode="overlay")
    # fig2.update_traces(color="quartilemethod")

    fig2.update_layout(paper_bgcolor="gray")

    return fig, fig2

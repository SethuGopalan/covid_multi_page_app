from numpy import equal, isin
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from dash import Dash, html, dcc, callback
import dash
from dash import Input, Output, dash_table
import numpy as np
import pandas as pd
from pytz import country_names
import requests
import time

import dash_bootstrap_components as dbc


from dash_labs.plugins.pages import register_page

# data section
register_page(__name__, path="/")
#  data for Geo Map
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
new_data = new_data.reset_index(drop=True)
dff_data = new_data[['continent', 'countries']]

url = 'https://disease.sh/v3/covid-19/countries'
r = requests.get(url)
con_data = r.json()


newCon_data = pd.DataFrame(con_data)


layout = html.Div([
    # header section

    dbc.Row([
        dbc.Col(html.H3('Covid Data Dashboard',
                className='text-center text-info, mb-4'))
    ]),
    html.Br(),
    # Dropdown
    dbc.Row([
            # ''' drop down for geo map''',
            dbc.Col([
                dcc.Dropdown(
                    id="my_dropdown", style={'color': 'gold', 'background': 'black'},
                    options=[{'label': i, 'value': i}
                             for i in data2.unique()],

                    value=["USA"],
                    multi=True,),
                html.Br(),
                html.Div(''' Coronavirus (COVID-19) Update: FDA Recommends Inclusion of Omicron BA.4/5 Component
                             for COVID-19 Vaccine Booster Doses'''),
            ], width={'size': 5, 'offset': 1}, style={'font': 'Cursive'}),

            dbc.Col([
                    html.Div('''COVID-19 is caused by a coronavirus called SARS-CoV-2.
                    Older adults and people who have severe underlying medical conditions
                    like heart or lung disease or diabetes seem to be at higher risk for
                    developing more serious complications from COVID-19 illness'''),

                    ], width={'size': 5, 'offset': 0}),
            ], style={"border": "4px black outset", 'font-family': 'Cursive'}),

    html.Br(),
    dbc.Row([
        dbc.Col([
            # ''' drop down for live data Continental''',
            html.Div('''Todays update by continent ''', style={
                'color': 'gold', 'fontSize': 18}),
            dcc.Dropdown(
                id="new_dropdown", style={'color': 'black'},
                options=[{'label': x, 'value': x}
                         for x in new_data['continent']],

                value="Asia",
                # multi=True,
            ),
        ], width={'size': 2, 'offset': 6}),

        dbc.Col([
            # ''' dropdown for live update country''',
            html.Div('''Todays update by country ''', style={
                'color': 'gold', 'fontSize': 18}),
            dcc.Dropdown(
                id="country_dropdown", style={'color': 'black'},
                options=[{'label': x, 'value': x}
                         for x in newCon_data['country']],

                value="India",
                # multi=True,
            ),
        ], width={'size': 2, 'offset': 0}),

    ], justify='center'),


    html.Br(),

    dbc.Row([
        # ''' div for picture''',
        dbc.Col([
            html.Div(html.Img(src=dash.get_asset_url(
                'immune-response-pri-new.jpg')), style={'height': '5%', 'width': '5%'}),
        ], width={'size': 2, 'offset': 1}),
    ]),

    dbc.Row([
        # '''colum for geo graph''',
        dbc.Col([

            dcc.Graph(id="graph1"),
        ], width={'size': 5, 'offset': 1}, style={"border": "1px white ridge"}),


        dbc.Col([
            # ''' Div for live update continantal''',

            html.Div(id='new_div', style={
                        'color': 'green', 'fontSize': 18}),
            html.Div(id='new_div1'),
            html.Div(id='new_div2'),
            html.Div(id='new_div3'),
            html.Div(id='new_div4'),
            html.Div(id='new_div5'),
            html.Div(id='new_div6'),
            html.Div(id='new_div7'),
            html.Div(id='new_div8')

        ], width={'size': 2, 'offset': 1}, style={"border": "1px white ridge"}),
        dbc.Col([
            # ''' Div for live update continantal''',

            html.Div(id='newCon_div', style={
                        'color': 'green', 'fontSize': 18}),
            html.Div(id='newCon_div1'),
            html.Div(id='newCon_div2'),
            html.Div(id='newCon_div3'),
            html.Div(id='newCon_div4'),
            html.Div(id='newCon_div5'),
            html.Div(id='newCon_div6'),
            html.Div(id='newCon_div7'),
            html.Div(id='newCon_div8')

        ], width={'size': 2, 'offset': 0}, style={"border": "1px white ridge"}),

    ]),

    html.Br(),



])


@ callback(Output("graph1", "figure"), Input("my_dropdown", "value"))
def filter_scatter(country):

    dff = df[df['iso_alpha_3'].isin(country)]
    fig = px.scatter_geo(dff, locations='iso_alpha_3',  color="iso_alpha_3", hover_name='iso_alpha_3', hover_data=['deaths', 'date', 'confirmed', 'recovered'], animation_group='iso_alpha_3'

                         )
    fig.update_traces(marker=dict(size=20), showlegend=True,
                      selector=dict(type='scattergeo'), mode='lines+markers+text')
    return fig


@ callback(Output("new_div", "children"),
           Output("new_div1", "children"),
           Output("new_div2", "children"),
           Output("new_div3", "children"),
           Output("new_div4", "children"),
           Output("new_div5", "children"),
           Output("new_div6", "children"),
           Output("new_div7", "children"),
           Input("new_dropdown", "value"))
def filter_scatter(cont_value):
    d_data = new_data[new_data['continent'] == cont_value]
    # d_data_d = d_data.reset_index(drop=True)

    return html.Div([html.P('{} '.format(d_data['continent'].str.upper().to_string(index=False))), html.Br()]), html.Div([html.P('Covid Cases : {}'.format(d_data['cases'].to_string(index=False)))]), html.Div([html.P('Today Cases :{}'.format(d_data['todayCases'].to_string(index=False)))]), html.Div([html.P('Critical : {} '.format(d_data['critical'].to_string(index=False)))]), html.Div([html.P('Deaths :{}'.format(d_data['deaths'].to_string(index=False)))]), html.Div([html.P('Todays Deaths :{}'.format(d_data['todayDeaths'].to_string(index=False)))]), html.Div([html.P('Today Recovered :{}'.format(d_data['todayRecovered'].to_string(index=False)))]), html.Div([html.P('Tests :{}'.format(d_data['tests'].to_string(index=False)))]),


@ callback(Output("newCon_div", "children"),
           Output("newCon_div1", "children"),
           Output("newCon_div2", "children"),
           Output("newCon_div3", "children"),
           Output("newCon_div4", "children"),
           Output("newCon_div5", "children"),
           Output("newCon_div6", "children"),
           Output("newCon_div7", "children"),
           Input("country_dropdown", "value"))
def filter_scatter(conNew_value):
    d_ConData = newCon_data[newCon_data['country'] == conNew_value]
    # d_data_d = d_data.reset_index(drop=True)

    return html.Div([html.P('{} '.format(d_ConData['country'].str.upper().to_string(index=False))), html.Br()]), html.Div([html.P('Covid Cases : {}'.format(d_ConData['cases'].to_string(index=False)))]), html.Div([html.P('Today Cases :{}'.format(d_ConData['todayCases'].to_string(index=False)))]), html.Div([html.P('Critical : {} '.format(d_ConData['critical'].to_string(index=False)))]), html.Div([html.P('Deaths :{}'.format(d_ConData['deaths'].to_string(index=False)))]), html.Div([html.P('Todays Deaths :{}'.format(d_ConData['todayDeaths'].to_string(index=False)))]), html.Div([html.P('Today Recovered :{}'.format(d_ConData['todayRecovered'].to_string(index=False)))]), html.Div([html.P('Tests :{}'.format(d_ConData['tests'].to_string(index=False)))]),

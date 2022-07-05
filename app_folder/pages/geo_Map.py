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
import datetime

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
                    id="my_dropdown", style={'color': 'gold', 'background': 'black', 'border': "1px black groove"},
                    options=[{'label': i, 'value': i}
                             for i in newCon_data['country']],

                    value=["UK", 'USA', 'China', 'India', 'Russia'],
                    multi=True,),
                html.Br(),
                html.Marquee(''' Coronavirus (COVID-19) Update: FDA Recommends Inclusion of Omicron BA.4/5 Component
                             for COVID-19 Vaccine Booster Doses''' 'Todays Covid case update for {} Todays cases {} Todats Deaths Today Recovered {}'.format(new_data['continent'][0], new_data['todayCases'][0], new_data['todayCases'][0], new_data['todayDeaths'][0], new_data['todayRecovered'][0], new_data['continent'][1], new_data['todayCases'][1], new_data['todayCases'][1], new_data['todayDeaths'][1], new_data['todayRecovered'][1])),
            ], width={'size': 5, 'offset': 1}, style={'font': 'Cursive'}),

            dbc.Col([
                    html.Div('''COVID-19 is caused by a coronavirus called SARS-CoV-2.
                    Older adults and people who have severe underlying medical conditions
                    like heart or lung disease or diabetes seem to be at higher risk for
                    developing more serious complications from COVID-19 illness'''),

                    ], width={'size': 5, 'offset': 0}),
            ], style={"border": "1px black groove", 'font-family': 'Cursive'}),

    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(html.Img(src=dash.get_asset_url(
                'immune-response-pri-latest.jpg')), style={'height': '5%', 'width': '5%'}),
        ], width={'size': 2, 'offset': 0}, style={"border": "1px black groove"}),
        dbc.Col([
            # ''' drop down for live data Continental''',
            html.Div('''Todays update by continent ''', style={
                'color': 'brown', 'fontSize': 18, 'font-family': 'Cursive'}),
            dcc.Dropdown(
                id="new_dropdown", style={'color': 'blue', 'background': 'black', 'border': "1px black groove"},
                options=[{'label': x, 'value': x}
                         for x in new_data['continent']],

                value="Asia",
                # multi=True,
            ),
        ], width={'size': 2, 'offset': 3}),

        dbc.Col([
            # ''' dropdown for live update country''',
            html.Div('''Todays update by country ''', style={
                'color': 'brown', 'fontSize': 18, 'font-family': 'Cursive'}),
            dcc.Dropdown(
                id="country_dropdown", style={'color': 'blue', 'background': 'black', 'border': "1px black groove"},
                options=[{'label': x, 'value': x}
                         for x in newCon_data['country']],

                value="India",
                # multi=True,
            ),
        ], width={'size': 2, 'offset': 1}),

    ], justify='center', style={"border": "1px black groove", }),


    html.Br(),

    dbc.Row([
        # ''' div for picture''',

    ]),

    dbc.Row([
        # '''colum for geo graph''',
        dbc.Col([

            dcc.Graph(id="graph1"),
        ], width={'size': 5, 'offset': 1}, style={"border": "1px black groove"}),


        dbc.Col([
            # ''' Div for live update continantal''',

            html.Div(id='new_div', style={
                        'color': 'green', 'fontSize': 18}),
            html.Div(id='new_div1', style={'font-family': 'Cursive'}),
            html.Div(id='new_div2', style={'font-family': 'Cursive'}),
            html.Div(id='new_div3', style={'font-family': 'Cursive'}),
            html.Div(id='new_div4', style={'font-family': 'Cursive'}),
            html.Div(id='new_div5', style={'font-family': 'Cursive'}),
            html.Div(id='new_div6', style={'font-family': 'Cursive'}),
            html.Div(id='new_div7', style={'font-family': 'Cursive'}),
            html.Div(id='new_div8', style={'font-family': 'Cursive'})

        ], width={'size': 2, 'offset': 1}, style={"border": "1px black groove"}),
        dbc.Col([
            # ''' Div for live update continantal''',

            html.Div(id='newCon_div', style={
                        'color': 'green', 'fontSize': 18}),
            html.Div(id='newCon_div1', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div2', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div3', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div4', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div5', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div6', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div7', style={'font-family': 'Cursive'}),
            html.Div(id='newCon_div8', style={'font-family': 'Cursive'})

        ], width={'size': 2, 'offset': 0}, style={"border": "1px black groove"}),
        dbc.Col([
            html.Div(id='latest-timestamp',
                     style={"padding": "20px"}),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,
                n_intervals=0
            ),
        ], width={'size': 4, 'offset': 8})

    ], style={"border": "1px black groove"}),

    html.Br(),



])


@ callback(Output("graph1", "figure"), Input("my_dropdown", "value"))
def filter_scatter(country):

    dff = newCon_data[newCon_data['country'].isin(country)]
    # fig = px.scatter_geo(dff, locations='country',  color='country',  hover_data=['updated', 'country', 'countryInfo', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'todayRecovered', 'active', 'critical', 'casesPerOneMillion', 'deathsPerOneMillion', 'tests', 'testsPerOneMillion', 'population', 'continent']
    #                      )
    fig = px.choropleth(dff, locations='country', locationmode="country names", color='country',
                        color_continuous_scale="Viridis",
                        animation_group='country',
                        range_color=(0, 12),
                        projection='robinson',
                        scope="world",
                        hover_data=['updated', 'country', 'countryInfo', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'todayRecovered',
                                    'active', 'critical',   'tests', 'population', 'continent'],
                        # mapbox_style="carto-positron",
                        # zoom=0,
                        # opacity=0.5,
                        #    labels={'unemp':'unemployment rate'}
                        # geojson='country'
                        # facet_row='country'
                        )
    fig.update_traces(marker=dict(size=20), showlegend=True,
                      selector=dict(type="carto-positron"), mode='lines+markers+text')
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

    return html.Div([html.P('{} '.format(d_data['continent'].str.upper().to_string(index=False))), html.Br()]), html.Div([html.P('Covid Cases : {}'.format(d_data['cases'].to_string(index=False)))]), html.Div([html.P('Today Cases : {}'.format(d_data['todayCases'].to_string(index=False)))]), html.Div([html.P('Critical : {} '.format(d_data['critical'].to_string(index=False)))]), html.Div([html.P('Deaths : {}'.format(d_data['deaths'].to_string(index=False)))]), html.Div([html.P('Todays Deaths : {}'.format(d_data['todayDeaths'].to_string(index=False)))]), html.Div([html.P('Today Recovered : {}'.format(d_data['todayRecovered'].to_string(index=False)))]), html.Div([html.P('Tests : {}'.format(d_data['tests'].to_string(index=False)))]),


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

    return html.Div([html.P('{} '.format(d_ConData['country'].str.upper().to_string(index=False))), html.Br()]), html.Div([html.P('Covid Cases : {}'.format(d_ConData['cases'].to_string(index=False)))]), html.Div([html.P('Today Cases : {}'.format(d_ConData['todayCases'].to_string(index=False)))]), html.Div([html.P('Critical : {} '.format(d_ConData['critical'].to_string(index=False)))]), html.Div([html.P('Deaths : {}'.format(d_ConData['deaths'].to_string(index=False)))]), html.Div([html.P('Todays Deaths : {}'.format(d_ConData['todayDeaths'].to_string(index=False)))]), html.Div([html.P('Today Recovered : {}'.format(d_ConData['todayRecovered'].to_string(index=False)))]), html.Div([html.P('Tests : {}'.format(d_ConData['tests'].to_string(index=False)))]),


@callback(
    [Output('latest-timestamp', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_timestamp(interval):
    return [html.Div(f"Last updated: {datetime.datetime.now()}")]

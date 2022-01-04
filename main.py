"""



Auteurs :Loqman Kalfaoui Samuel Bury
Date : 03/01/2022
"""

### Imports ###
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html


# dataset initial
mortality = pd.read_csv("countries of the world.csv")
# lien : https://www.kaggle.com/komalkhetlani/infant-mortality
# Pour ajouter les coordonnées à notre dataframe :
coordonates = pd.read_csv('country-coordinates-world.csv')
# lien : https://www.kaggle.com/vinitasilaparasetty/country-coordinates-world

# 1. Traitons la dataset des mortalités

mortality = mortality.drop(['Region'], 1)
mortality = mortality.drop(['Coastline (coast/area ratio)'], 1)
mortality = mortality.drop(['Literacy (%)'], 1)
mortality = mortality.drop(['Phones (per 1000)'], 1)
mortality = mortality.drop(['Arable (%)'], 1)
mortality = mortality.drop(['Crops (%)'], 1)
mortality = mortality.drop(['Other (%)'], 1)
mortality = mortality.drop(['Climate'], 1)
mortality = mortality.drop(['Birthrate'], 1)
mortality = mortality.drop(['Deathrate'], 1)
mortality = mortality.drop(['Agriculture'], 1)
mortality = mortality.drop(['Industry'], 1)
mortality = mortality.drop(['Service'], 1)

coordonates['Country'] = coordonates['Country'] + " "

df = pd.merge(coordonates, mortality, how='left', on=['Country'])

df['Population'].fillna('XX', inplace=True)
df = df[df['Population'] != 'XX']

maindf = df[df['Population'] > 100000000]
map = go.Figure(
    go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['Country'] + '<br>Population ' + (df['Population']/1e6).astype(str)+' million' + '<br>Mortalité Infantile ' + df['Infant mortality (per 1000 births)'].astype(str)+' ‰',
        marker = dict(
            color = "royalblue",
            size= 7,#int(df['Population'] / 5000),
            opacity = 0.5,
            reversescale = True,
            autocolorscale = True,
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
    )
)

histoPop = px.bar(df, y='Population', x='Country', text_auto='.2s',
            title="Histogramme de la population des pays du monde ")
histoDensity = px.bar(maindf, x="Country", y="Pop. Density (per sq. mi.)", text_auto='.2s',
            title="Histogramme de la densité des pays du monde ")

chart = {
    'background': '#BD99D2',
    'text': '#111111',
    'legend': '#27BBE8',
    'title': '#111111'
}

# On créé une instance de la classe dash
app = dash.Dash(__name__)


# On créé le titre du dashboard
app.title = 'Dashbord Mortality'


app.layout = html.Div([

        ### Titre ###
        html.Br(),
        html.H1(children=
            'Dashboard sur la mortalité infantile ',
            style={'textAlign': 'center', 'color': chart['title']}
        ),
        html.P("Cette carte répertorie les pic de population dans le monde"),
        dcc.Graph(
            id='1',
            figure=map
        ),
        dcc.Graph(
            id='2',
            figure=histoPop
        ),
        dcc.Graph(
            id='3',
            figure=histoDensity
        )
    ]
)






if __name__ == '__main__':
    app.run_server(debug=True)


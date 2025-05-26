import dash
from dash import html, dcc,Input,Output,callback
import pandas
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

data=pandas.read_csv("/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv")
data1=pandas.read_csv("/home/batuhan-saylam/Downloads/HDR21-22_Composite_indices_complete_time_series.csv")
data=data.merge(data1[["iso3","country"]],how="inner",on="country")

load_figure_template("slate")
dash.register_page(__name__, path='/home')
fig=px.choropleth(template="slate")
fig.update_geos(projection_type="miller",visible=False,resolution=50,showcountries=True,scope="world")
fig.update_layout(height=1000, margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)')
fig2=px.line(template="slate")
fig2.update_layout(height=500,margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig15 = px.histogram(data, x="Region")
fig15.update_layout(height=400)
layout = html.Div(children=[
    html.Div([dcc.Graph(id="mapgraph",figure=fig)
              ],style={"width":"80%","float":"right",'display':'inline-block'}),
    html.Div([
        "Harita ve bar grafiği için değişken seç:",
        dcc.Dropdown(data.columns.unique(),id="x",style={'background-color':'#D62728', 'margin':'0 auto'})],style={"width":"15%",'display':'inline-block'}),
    html.Div([
        "Bar grafiği için bölge seç:",
        dcc.Dropdown(data["Region"].unique().tolist(),id="country",style={'background-color':'#D62728', 'margin':'0 auto'})
    ],style={"width":"15%",'display':'inline-block'}),
    html.Div([
        "Scope seç:",
       dcc.Dropdown(['africa', 'asia', 'europe', 'north america', 'south america', 'usa', 'world'],id="scope",style={'background-color':'#D62728', 'margin':'0 auto'})
    ],style={"width":"15%",'display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Graph(id="scatters",figure=fig2)
        ]),
        html.Div([
            dcc.Graph(figure=fig15)
        ])

    ],style={"width":"15%","float":"left",'display':'inline-block'})


])
@callback(
    Output("mapgraph","figure"),
    Input("x","value"),
    Input("scope","value")
)
def map_plot(x,sc):
    fig = px.choropleth(data, locations="iso3",
                        color=x, # lifeExp is a column of gapminder
                        color_continuous_scale="Solar",
                        hover_name="country", # column to add to hover information,
                        template="slate"
                    )
    fig.update_geos(projection_type="miller",visible=False,resolution=50,showcountries=True,scope=sc)
    fig.update_layout(height=1000,margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)')
    return fig
@callback(
    Output("scatters","figure"),
    Input("x","value"),
    Input("country","value"),
)
def timeseries(var1,cou):
    data2=data[data["Region"]==cou]
    fig=px.bar(x= data2["country"],y=data2[var1],template="slate",color_discrete_sequence =["goldenrod"])
    fig.update_layout(height=400,margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig
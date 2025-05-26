import dash
from dash import html, dcc,Input,Output,callback
import pandas
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import seaborn as sn
import numpy as np
import plotly.figure_factory as ff
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
load_figure_template("slate")
data=pandas.read_csv("/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv")
data1=pandas.read_csv("/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/HDR21-22_Composite_indices_complete_time_series.csv")
data=data.merge(data1[["iso3","country"]],how="inner",on="country")
data11=pandas.read_csv("/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv")

dash.register_page(__name__, path='/enve')

layout=html.Div([
    html.Div([
        "Bölge seç:",
        dcc.Dropdown(data["Region"].unique().tolist(),id="Regions")
    ]),
    html.Div([
        dcc.Graph(id="energy")
    ]),
    html.Div([
        dcc.Graph(id="pollution")
    ]),
    html.Div([
        dcc.Graph(id="thsp")
    ])
])
@callback(
    Output("energy","figure"),
    Input("Regions","value")
)
def renderplot(reg):
    data=data11[data11["Region"]==str(reg)]
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Scatter(x=data["country"], y=data['CO2 emission estimates (million tons/tons per capita)'], mode="lines",name="CO2 emisyon (milyon ton)"),
        secondary_y=True)
    fig1.add_trace(
        go.Bar(x=data["country"],y=data["Energy production, primary (Petajoules)"],name="Enerji Üretimi (Petajoules)"))
    fig1.update_layout(xaxis=dict(title="Ülkeler",),yaxis=dict(title="Enerji Üretimi (Petajoules)"),yaxis2=dict(title="CO2 emisyon(milyon ton)"))
    return fig1
@callback(
    Output("pollution","figure"),
    Input("Regions","value")
)
def renderplot2(reg):
    data=data11[data11["Region"]==str(reg)]
    fig = px.bar(data, x='country', y='Pollution index',
             hover_data=['Pollution index', 'Climate index'], color='Climate index',
             labels={'Pollution index':'Kirlilik indeksi',"country":"Ülkeler"}, height=400)
    return fig
@callback(
    Output("thsp","figure"),
    Input("Regions","value")
)
def renderplot3(reg):
    data=data11[data11["Region"]==str(reg)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["country"],
        y=data["Threatened species (number)"],
        name='control',
        marker_color='#EB89B5',
        opacity=0.75
    ))


    fig.update_layout(
        title_text='Ülkelere göre nesli tehlikede türler', # title of plot
        xaxis_title_text='Ülkeler', # xaxis label
        yaxis_title_text='Ülkedeki nesli tehlikede canlı sayısı', # yaxis label
)
    return fig
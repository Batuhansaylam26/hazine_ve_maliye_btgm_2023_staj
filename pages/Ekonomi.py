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

dash.register_page(__name__, path='/econ')

Q3,Q1=np.percentile(data["GDP: Gross domestic product (million current US$)"].tolist(),[75,25])
IQR=Q3-Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
 
# Create arrays of Boolean values indicating the outlier rows
upper_array = np.where(data["GDP: Gross domestic product (million current US$)"]>=upper)[0]
lower_array = np.where(data["GDP: Gross domestic product (million current US$)"]<=lower)[0]
 
# Removing the outliers
data.drop(index=upper_array, inplace=True)
data.drop(index=lower_array, inplace=True)


Q3,Q1=np.percentile(data["Population in thousands (2017)"].tolist(),[75,25])
IQR=Q3-Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
 
# Create arrays of Boolean values indicating the outlier rows
upper_array = np.where(data["Population in thousands (2017)"]>=upper)[0]
lower_array = np.where(data["Population in thousands (2017)"]<=lower)[0]
 
# Removing the outliers
data.drop(index=upper_array, inplace=True)
data.drop(index=lower_array, inplace=True)


import statsmodels.api as sm
X=data["Population in thousands (2017)"]
y=data["GDP: Gross domestic product (million current US$)"]


# Fit and summarize OLS model
mod = sm.OLS(y, X)
X = sm.add_constant(X)

res = mod.fit()

xrange=np.linspace(X["Population in thousands (2017)"].min(),X["Population in thousands (2017)"].max(),100)
pred=res.predict(xrange)
ressum=res.summary()

fig10 = go.Figure()
# Create and style traces
fig10.add_trace(go.Scatter(x=data["Population in thousands (2017)"],y=data["GDP: Gross domestic product (million current US$)"],mode="markers",marker=dict(color=data["GDP: Gross domestic product (million current US$)"],colorscale='viridis',showscale=True)))
fig10.add_trace(go.Scatter(x=xrange, y=pred, name = 'pe m',
                         line=dict(color='royalblue', width=4)))


# Edit the layoutGDP: Gross domestic product (million current US$)"],
fig10.update_layout(title='GDP vs Nüfuz',
                   xaxis_title='Nüfuz',
                   yaxis_title='GDP')


df2=data[["Region","GDP growth rate (annual %, const. 2005 prices)","GDP: Gross domestic product (million current US$)","Unemployment (% of labour force)","Purchasing Power Index","Inflation, consumer prices (annual %)"]]
fig2 = ff.create_scatterplotmatrix(df2, diag='histogram', index='Region',
                              colormap_type='seq', height=1000, width=1800)
fig2.update_layout(height=2000,margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)')

layout=html.Div([
    html.Div([
    "Regression Plot:"]),
    html.Div([
        dcc.Graph(figure=fig10)
    ],style={"width":"48%","display":"inline-block"}),
    html.Div([
        html.P(str(ressum))
    ],style={"width":"48%","float":"right","display":"inline-block"}),
    html.Div([
        "Bölge seç:",
        dcc.Dropdown(data["Region"].unique().tolist(),id="Regions")
    ]),
    html.Div([
        dcc.Graph(id="unemp")
    ]),
    "Bazı ekonomik göstergelerin Scatter Matrixi ",
    html.Br(),
    html.Div([
        dcc.Graph(figure=fig2)
    ])
])
@callback(
    Output("unemp","figure"),
    Input("Regions","value")
)
def renderplot(reg):
    data=data11[data11["Region"]==reg]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=data["country"], y=data["Unemployment (% of labour force)"], mode="lines",name="İşsizlik (% İş gücü)"),
        secondary_y=True
)
    fig.add_trace(go.Bar(
        x=data["country"],
        y=data["Employment: Agriculture (% of employed)"],
        name='İstihdam (Tarım)',
        marker_color='indianred'
))
    fig.add_trace(go.Bar(
        x=data["country"],
        y=data["Employment: Industry (% of employed)"],
        name='İstihdam (Sanayi )',
        marker_color='lightsalmon'
))
    fig.add_trace(go.Bar(
        x=data["country"],
        y=data["Employment: Services (% of employed)"],
        name='İstihdam (Hizmet ve diğer sektörler)',
        marker_color='royalblue'
))
    fig.update_layout(barmode='group', xaxis_tickangle=-45,
                    title='İstihdam ve İşsizlik Grafiği',
                   xaxis=dict(title='Ülkeler'),
                   yaxis=dict(title='İstihdam (% toplam istihdam)'),
                   yaxis2=dict(title="İşsizlik (% iç gücü)"))
    return fig

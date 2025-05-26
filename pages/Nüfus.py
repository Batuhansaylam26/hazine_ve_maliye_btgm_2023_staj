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
data1=pandas.read_csv("/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv")
data=data.merge(data1[["iso3","country"]],how="inner",on="country")
dash.register_page(__name__, path='/population')

data2=data[["country","Region","Population, male"]]
data2=data2.groupby(["Region"])["Population, male"].sum().reset_index()
data2=pandas.DataFrame(data2)
data2["gender"]=["male"]*len(data2)
data2.columns=["Region","count","gender"]
data2=data2.sort_values(by=["Region"])
data3=data[["country","Region","Population, female"]]
data3=data3.groupby(["Region"])["Population, female"].sum().reset_index()
data3=pandas.DataFrame(data3)
data3["gender"]=["female"]*len(data3)
data3.columns=["Region","count","gender"]
data3=data3.sort_values(by=["Region"])
data2=pandas.concat([data2,data3])
data2.sort_values(by=["Region"])
dicti={}
for i in data2["Region"].unique():
    data11=data2[data2["Region"]==i]
    dicti[i]=data11[data11["gender"]=="female"].values[0,1]/data11[data11["gender"]=="male"].values[0,1]
dicti=pandas.DataFrame.from_dict(dicti,orient="index").reset_index()
dicti.columns=["Region","ratio"]
data2=pandas.merge(data2,dicti,on="Region")
data2

fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(
    go.Scatter(x=dicti['Region'], y=dicti['ratio'], mode="lines",name="Kadın nüfusun erkek nüfusa oranı"),
    secondary_y=True
)

fig1.add_trace(
    go.Bar(x=data2[data2["gender"]=="male"]['Region'], y=data2[data2["gender"]=="male"]['count'],name="Erkek nüfus"),
    secondary_y=False
)


fig1.add_trace(
    go.Bar(x=data2[data2["gender"]=="female"]["Region"],y=data2[data2["gender"]=="female"]["count"],name="Erkek nüfus")
)

fig1.update_layout(barmode='stack',
                   xaxis=dict(title="Bölgeler"),
                   yaxis=dict(title="Nüfus (milyon)"),
                   yaxis2=dict(title="Kadın nüfusun erkek nüfusa oranı"))


x=data["Education: Primary gross enrol. ratio (f/m per 100 pop.)"].tolist()
f=[]
m=[]
for i in x:
    u=i.split("/")
    f.append(float(u[0]))
    m.append(float(u[1]))
data["Education: Primary gross enrol. ratio (f per 100 pop.)"]=f
data["Education: Primary gross enrol. ratio (m per 100 pop.)"]=m


x=data["Education: Secondary gross enrol. ratio (f/m per 100 pop.)"].tolist()
f=[]
m=[]
for i in x:
    u=i.split("/")
    f.append(float(u[0]))
    m.append(float(u[1]))
data["Education: Secondary gross enrol. ratio (f per 100 pop.)"]=f
data["Education: Secondary gross enrol. ratio (m per 100 pop.)"]=m


x=data["Education: Tertiary gross enrol. ratio (f/m per 100 pop.)"].tolist()
f=[]
m=[]
for i in x:
    u=i.split("/")
    f.append(float(u[0]))
    m.append(float(u[1]))
data["Education: Tertiary gross enrol. ratio (f per 100 pop.)"]=f
data["Education: Tertiary gross enrol. ratio (m per 100 pop.)"]=m



fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Primary gross enrol. ratio (f per 100 pop.)"].sum(), name='ilkokul (kadın)',
                         line=dict(color='firebrick', width=4)))
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Primary gross enrol. ratio (m per 100 pop.)"].sum(), name = 'ilkokul (erkek)',
                         line=dict(color='royalblue', width=4)))
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Secondary gross enrol. ratio (f per 100 pop.)"].sum(), name='Ortaokul (kadın)',
                         line=dict(color='firebrick', width=4,
                              dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
))
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Secondary gross enrol. ratio (m per 100 pop.)"].sum(), name='Ortaokul (erkek)',
                         line = dict(color='royalblue', width=4, dash='dash')))
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Tertiary gross enrol. ratio (f per 100 pop.)"].sum(), name='Yüksek öğretim (kadın)',
                         line = dict(color='firebrick', width=4, dash='dot')))
fig2.add_trace(go.Scatter(x=data["Region"].unique(), y=data.groupby("Region")["Education: Tertiary gross enrol. ratio (m per 100 pop.)"].sum(), name='(YÜksek öğretim erkek)',
                         line=dict(color='royalblue', width=4, dash='dot')))

# Edit the layout
fig2.update_layout(title='Bölgelere göre eğitim seviyeleri',
                   xaxis_title='Bölgeler',
                   yaxis_title='Eğitim:  kayıtlı oranı (100 kişi başına bir öğrenci)')





fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=data["Region"].unique(),
    y=data.groupby("Region")["Population in thousands (2017)"].sum(),
    name="Nüfus verisi"
))


fig3.add_trace(go.Scatter(
    x=data["Region"].unique(),
    y=data.groupby("Region")["Fertility rate, total (live births per woman)"].sum(),
    name="Doğum oranı, toplam (kadın başına canlı doğum )",
    yaxis="y2"
))



# Create axis objects
fig3.update_layout(
    xaxis=dict(
        domain=[0.3, 0.7]
    ),
    yaxis=dict(
        title="Nüfus (Bin) (2017)",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
    ),
    yaxis2=dict(
        title="Doğum oranı, toplam (kadın başına canlı doğum ) ",
        titlefont=dict(
            color="#ff7f0e"
        ),
        tickfont=dict(
            color="#ff7f0e"
        ),
        anchor="x",
        overlaying="y",
        side="right",
        position=0.15
    )
)

# Update layout properties
fig3.update_layout(
    title_text="Bölgeler göre doğum oranı ve nüfus grafiği",
    width=800,
)

layout=html.Div([
    html.Div([
        "Bölge/Bölgeler seç:",
        dbc.Checklist(options=['SouthAmerica', 'Oceania', 'WesternEurope', 'EasternEurope','SouthernEurope', 'NorthernAmerica', 'EasternAsia', 'WesternAsia','NorthernEurope', 'NorthernAfrica', 'SouthernAsia','South-easternAsia', 'CentralAmerica', 'SouthernAfrica']
,id="memory",inline=True),
        dcc.Graph(id="pop-traffic")
    ]),
    html.Div([
        dcc.Graph(figure=fig1),
        "En çok kadın ve erkek nüfuzu Güney Asya'da olsa da kadın nüfusun erkeğe göre en fazla olduğu bölge Doğu Avrupa. En az erkek ve kadın nüfusunun olduğu bölge ise Okyanusya olurken kadın nüfusunun erkeğe göre en az olduğu bölge Batı Asya."
    ]),
    html.Div([
        dcc.Graph(figure=fig2),
        "En yüksek kadın ve erkek ilkokul ve yüksek öğretim eğitimleri Batı Avrupa, orta okul eğitimleri Kuzey Amerika bölgelerindedir. Diğer bir yandan, üç eğitim seviyesi için de en düşük eğitim nüfuzuna sahip ülkeler Kuzey Afrika bölgesindedir. "
    ]),
    html.Div([
        dcc.Graph(figure=fig3),
        "En yüksek doğum oranı Orta Amerika bölgesinde olmasına rağmen en fazla nüfusa sahip ülkeler Güney Asya'dadır. En düşük nüfus ise Güney Avrupa'da olmasına rağmen en düşük doğum oranı da Doğu Asya'dadır."
    ])
])

@callback(
    Output("pop-traffic","figure"),
    [Input("memory","value")]
)
def scline(reg):
    data1=pandas.DataFrame(columns=data.columns.tolist())
    for i in reg:
        data1=data1.append(data[data["Region"]==i])
    fig = px.scatter(data1, x="Population density (per km2, 2017)", y="Traffic commute time index", marginal_x="box", marginal_y="violin",color="Region")
    fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
    return fig 





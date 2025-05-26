import dash
from dash import html, dcc, Input, Output, callback
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
import statsmodels.api as sm

load_figure_template("slate")
data = pandas.read_csv(
    "/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv"
)
data1 = pandas.read_csv(
    "/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/HDR21-22_Composite_indices_complete_time_series.csv"
)
data = data.merge(data1[["iso3", "country"]], how="inner", on="country")
dash.register_page(__name__, path="/trading")
fig = make_subplots(
    rows=1,
    cols=2,
    specs=[[{}, {}]],
    shared_xaxes=True,
    shared_yaxes=False,
    vertical_spacing=0.001,
)
fig.append_trace(
    go.Bar(
        y=data["Region"].unique(),
        x=data.groupby("Region")["Military expenditure (% of GDP)"].sum(),
        marker_color="indianred",
        orientation="h",
        name="Toplam savunma harcaması (% GDP)",
    ),
    1,
    1,
)
fig.add_trace(
    go.Bar(
        y=data["Region"].unique(),
        x=data.groupby("Region")["Health: Total expenditure (% of GDP)"].sum(),
        marker_color="rgba(246, 78, 139, 0.6)",
        orientation="h",
        name="Toplam sağlık harcaması (% GDP)",
    )
)


fig.append_trace(
    go.Line(
        y=data["Region"].unique(),
        x=data.groupby("Region")["Tax revenue (% of GDP)"].sum(),
        name="Vergi geliri (% GDP)",
    ),
    1,
    2,
)
fig.update_layout(
    barmode="stack",
    yaxis=dict(
        title="Ülkeler",
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor="rgba(102, 102, 102, 0.8)",
        linewidth=2,
        domain=[0, 0.85],
    ),
    xaxis=dict(
        title="Harcamalar",
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        title="Vergi Geliri (% GDP)",
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side="top",
        dtick=25000,
    ),
    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor="rgb(248, 248, 255)",
    plot_bgcolor="rgb(248, 248, 255)",
)
data["Economy: Agriculture (% of GVA)"] = pandas.to_numeric(
    data["Economy: Agriculture (% of GVA)"], errors="coerce"
)
data = (
    data.groupby("Region")[
        [
            "Economy: Agriculture (% of GVA)",
            "Economy: Industry (% of GVA)",
            "Economy: Services and other activity (% of GVA)",
        ]
    ]
    .sum()
    .reset_index()
)

x = (
    data[
        [
            "Economy: Agriculture (% of GVA)",
            "Economy: Industry (% of GVA)",
            "Economy: Services and other activity (% of GVA)",
        ]
    ]
    .sum(axis=1)
    .tolist()
)
data["total"] = x
data.iloc[:, 1:] = data.iloc[:, 1:].div(data["total"], axis=0).mul(100).round(2)


fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=data["Economy: Agriculture (% of GVA)"],
        y=data["Region"].unique(),
        orientation="h",
        marker=dict(
            color="rgba(38, 24, 74, 0.8)", line=dict(color="rgb(248, 248, 249)")
        ),
        name="Tarım brüt katma değeri",
    )
)
fig1.add_trace(
    go.Bar(
        x=data["Economy: Industry (% of GVA)"],
        y=data["Region"].unique(),
        orientation="h",
        marker=dict(line=dict(color="rgb(248, 248, 249)")),
        name="Sanayi brüt katma değeri",
    )
)
fig1.add_trace(
    go.Bar(
        x=data["Economy: Services and other activity (% of GVA)"],
        y=data["Region"].unique(),
        orientation="h",
        marker=dict(line=dict(color="rgb(248, 248, 249)")),
        name="Hizmet ve diğer sektörlerin brüt katma değeri",
    )
)
fig1.update_layout(
    xaxis_title="Toplam brüt katma değerdeki pay",
    yaxis_title="Bölgeler",
    barmode="stack",
)


data = pandas.read_csv(
    "/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv"
)

fig3 = px.treemap(
    data,
    path=[px.Constant("world"), "Region", "country"],
    values="International trade: Exports (million US$)",
    color="International trade: Imports (million US$)",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=np.average(
        data["International trade: Imports (million US$)"]
    ),
)
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))

layout = html.Div(
    [
        html.Div(
            [
                html.Div(["Government Expend-Tex revenue"]),
                dcc.Graph(figure=fig),
                "En yüksek sağlık harcaması Güney Asya ve en yüksek askeri harcama ise Orta Amerika bölgesindedir. En düşük askeri harcama Kuzey Afrika'da iken en düşük sağlık harcaması Doğu Avrupa'dadır.Ek olarak en çok vergi toplayan ülkeler Kuzey Amerika'da ve en düşük vergi toplayan ülkeler ise Güney Amerika'dadır.",
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(["the percent of econ"]),
                        dcc.Graph(figure=fig1),
                        "Ekonomisi içinde Tarım sektörü en çok yere sahip olan ülkeler Güney Asyada iken en düşüş paya sahip olan ülkeler Kuzey Amerika'dadır. Ekonomisi içinde en büyük paya sanayisi sahip olan ülkeler Kuzey Afrika'da iken en düşük paya sahip Batı Avrupa'dadır. Ekonomisi içinde hizmet ve diğer sektörler tarafından en büyük paya sahip olan ülkeler Batı Avrupa'da iken en düşük paya sahip ülkeler Güney Doğu Asya'dır. ",
                    ]
                ),
                html.Div(
                    [
                        "İhracat-ithalat şeması:",
                        dcc.Graph(figure=fig3),
                        "En fazla ihracat yapan ülke ABD olmasına rağmen en yüksek ihracat yapan ülke Çin'dir. En düşük ithalat ve ihracat yapan ülke ise Kıbrıs'dır. ",
                    ]
                ),
            ]
        ),
    ]
)

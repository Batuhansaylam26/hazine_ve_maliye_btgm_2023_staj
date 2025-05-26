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
import statsmodels.formula.api as smf

load_figure_template("slate")
data = pandas.read_csv(
    "/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/soci_econ_country_profiles.csv"
)
data1 = pandas.read_csv(
    "/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/data/HDR21-22_Composite_indices_complete_time_series.csv"
)
data = data.merge(data1[["iso3", "country"]], how="inner", on="country")
dash.register_page(__name__, path="/health")
data5 = data
data6 = data
data["Health: Physicians (per 1000 pop.)"] = pandas.to_numeric(
    data["Health: Physicians (per 1000 pop.)"], errors="coerce"
)


data6 = data6[
    [
        "Infant mortality rate (per 1000 live births",
        "Health: Physicians (per 1000 pop.)",
        "Health: Total expenditure (% of GDP)",
    ]
]
data6.columns = ["infant", "physician", "expenditure"]


model = smf.ols(formula="infant ~ physician + expenditure", data=data6)
results = model.fit()
summ = results.summary()
x, y = model.exog_names[1:]

x_range = np.arange(data6[x].min(), data6[x].max())
y_range = np.arange(data6[y].min(), data6[y].max())

X, Y = np.meshgrid(x_range, y_range)

exog = pandas.DataFrame({x: X.ravel(), y: Y.ravel()})
Z = results.predict(exog=exog).values.reshape(X.shape)

fig = px.scatter_3d(data6, x="physician", y="expenditure", z="infant")
fig.update_traces(marker=dict(size=5))
fig.add_traces(go.Surface(x=X, y=Y, z=Z, name="pred_surface"))
fig.update_layout(
    height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor="rgba(0,0,0,0)"
)


from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def format_coefs(coefs):
    equation_list = [f"{coef}x^{i}" for i, coef in enumerate(coefs)]
    equation = "$" + " + ".join(equation_list) + "$"

    replace_map = {"x^0": "", "x^1": "x", "+ -": "- "}
    for old, new in replace_map.items():
        equation = equation.replace(old, new)

    return equation


fig31 = px.line(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].mean()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].mean()["Life expectancy at birth, female (years)"],
    title="Ortalama",
)
fig31.add_bar(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].mean()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].mean()["Life expectancy at birth, male (years)"],
)


fig32 = px.line(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].max()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].max()["Life expectancy at birth, female (years)"],
    title="Maximum",
)
fig32.add_bar(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].max()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].max()["Life expectancy at birth, male (years)"],
)

fig33 = px.line(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].min()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, female (years)"
    ].min()["Life expectancy at birth, female (years)"],
    title="Minimum",
)
fig33.add_bar(
    x=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].min()["Region"],
    y=data5.groupby("Region", as_index=False)[
        "Life expectancy at birth, male (years)"
    ].min()["Life expectancy at birth, male (years)"],
)


layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(figure=fig31),
                        "Erkekler için ortalama tahmini ömür süresinin en fazla olduğu ülke Okyanusya bölgesinde iken kadınlar için ortalama tahmini ömür süresinin en fazla olduğu ülke Kuzey Amerika bölgesindedir. Erkekler için ortalama tahmini ömür süresinin en az olduğu ülke Güney Afrika bölgesinde iken kadınlar için ortalama tahmini ömür süresinin en az olduğu ülke de Güney Afrika bölgesindedir.",
                    ],
                    style={"width": "33%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Graph(figure=fig32),
                        "Erkekler için maksimum tahmini ömür süresinin en fazla olduğu ülke Doğu Avrupa bölgesinde iken kadınlar için maksimum tahmini ömür süresinin en fazla olduğu ülke Doğu Asya bölgesindedir.Erkekler için maksimum tahmini ömür süresinin en az olduğu ülke Güney Afrika bölgesinde iken kadınlar için maksimum tahmini ömür süresinin en az olduğu ülke Güney Afrika bölgesindedir. ",
                    ],
                    style={"width": "33%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Graph(figure=fig33),
                        "Erkekler için minimum tahmini ömür süresinin en fazla olduğu ülke Okyanusya bölgesinde iken kadınlar için minimum tahmini ömür süresinin en fazla olduğu ülke Kuzey Amerika bölgesindedir.Erkekler için minimum tahmini ömür süresinin en az olduğu ülke Güney Afrika bölgesinde iken kadınlar için minimum tahmini ömür süresinin en az olduğu ülke Güney Afrika bölgesindedir. ",
                    ],
                    style={"width": "33%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [html.Div([dcc.Graph(figure=fig)])],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [html.P(children=str(summ))],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
    ]
)

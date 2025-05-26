import dash
from dash import html, dcc, Input, Output, callback, dash_table
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
dash.register_page(__name__, path="/data")


df = data[
    [
        "Region",
        "Population in thousands (2017)",
        "GDP: Gross domestic product (million current US$)",
        "Unemployment (% of labour force)",
        "International trade: Exports (million US$)",
        "Seats held by women in national parliaments %",
        "CO2 emission estimates (million tons/tons per capita)",
        "Energy supply per capita (Gigajoules)",
        "Quality Of Life Index",
        "Purchasing Power Index",
        "Safety Index",
        "Inflation, consumer prices (annual %)",
    ]
]
df_corr = df.corr(numeric_only=True)
fig = px.imshow(df_corr, text_auto=True)
fig.update_layout(height=1000)


layout = html.Div(
    [
        html.Div(
            [
                dash_table.DataTable(
                    id="datatable-interactivity",
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True}
                        for i in data.columns
                    ],
                    data=data.to_dict("records"),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current=0,
                    page_size=10,
                )
            ]
        ),
        html.Div(children=["Correlation Heat Map", html.Div([dcc.Graph(figure=fig)])]),
    ]
)

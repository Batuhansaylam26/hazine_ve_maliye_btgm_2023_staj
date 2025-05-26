import dash
from dash import html, dcc,Input,Output,callback

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")

dash.register_page(__name__, path='/content')
layout=html.Div([
    html.H3(
        """Content"""),
    html.P("""
This dataset contains about 95 statistical indicators of the 66 countries. It covers a broad spectrum of areas including:"""),
    html.P("""
-General Information"""),
    html.P("""
-Broader Economic Indicators"""),
    html.P("""
-Social Indicators"""),
    html.P("""
-Environmental & Infrastructure Indicators"""),
    html.P("""
-Military Spending"""),
    html.P("""
-Healthcare Indicators"""),
    html.P("""
-Trade Related Indicators e.t.c."""),
    html.P("""
This data-set for the year 2017 is an amalgamation of data from SRK's Country Statistics - UNData, Numbeo and World Bank."""
), 
    html.P(
        """Additional data such as "Cost of living index", "Property price index", "Quality of life index" have been extracted from Numbeo and a number of metrics related to "trade", "healthcare", "military spending", "taxes" etc are extracted from World Bank data source."""),
    html.P("""        
Given that this is an amalgamation of data from three different sources, only those countries(about 66) which have sufficient data across all the three sources are considered."""
    )
])
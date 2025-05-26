from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="/home/batuhansaylam/Desktop/hazine_ve_maliye_btgm_2023_staj/pages",
    external_stylesheets=[dbc.themes.CYBORG],
)


app.layout = html.Div(
    [
        dbc.NavbarSimple(
            [
                dbc.NavItem(dbc.NavLink("Harita", href="/home")),
                dbc.NavItem(dbc.NavLink("Veri", href="/data")),
                dbc.NavItem(dbc.NavLink("Sağlık", href="/health")),
                dbc.NavItem(dbc.NavLink("Nüfus", href="/population")),
                dbc.NavItem(dbc.NavLink("Ticaret", href="/trading")),
                dbc.NavItem(dbc.NavLink("Ekonomi", href="/econ")),
                dbc.NavItem(dbc.NavLink("Çevre", href="/enve")),
                dbc.NavItem(dbc.NavLink("Veri Hakkında", href="/content")),
            ],
            brand="SOSYO-EKONOMIK VERI ANALIZI",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        html.Br(),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run(debug=True)

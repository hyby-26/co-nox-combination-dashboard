import dash
from dash import html

dash.register_page(__name__, path="/new", name="새 페이지")

layout = html.Div(
    html.Div("준비 중입니다.", className="content-card"),
    className="app-shell",
)

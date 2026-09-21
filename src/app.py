import dash
from dash import Dash, Input, Output, State, dcc, html

app = Dash(__name__, use_pages=True)

SUN_ICON = html.Img(
    src=app.get_asset_url("icons/sun.svg"), className="icon-sun", alt=""
)
MOON_ICON = html.Img(
    src=app.get_asset_url("icons/moon.svg"), className="icon-moon", alt=""
)


def _page_nav():
    links = [
        dcc.Link(page["name"], href=page["relative_path"], className="page-nav-link")
        for page in dash.page_registry.values()
    ]
    return html.Div(links, className="page-nav")


app.layout = html.Div(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        html.Div(
            [
                html.Div(
                    [
                        html.H1("CO-NOx Combination Dashboard"),
                        html.Div(
                            "가스터빈 센서 데이터 · CO/NOX 배출 분석",
                            className="subtitle",
                        ),
                    ]
                ),
                html.Button(
                    [SUN_ICON, MOON_ICON],
                    id="theme-toggle",
                    className="theme-toggle",
                    n_clicks=0,
                    **{"aria-label": "다크 모드로 전환"},
                ),
            ],
            className="app-header",
        ),
        _page_nav(),
        dash.page_container,
    ]
)


app.clientside_callback(
    """
    function(n_clicks, current) {
        if (!n_clicks) { return current || 'light'; }
        return current === 'dark' ? 'light' : 'dark';
    }
    """,
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
)

app.clientside_callback(
    """
    function(theme) {
        var t = theme || 'light';
        document.documentElement.setAttribute('data-theme', t);
        return t === 'dark' ? '라이트 모드로 전환' : '다크 모드로 전환';
    }
    """,
    Output("theme-toggle", "aria-label"),
    Input("theme-store", "data"),
)


if __name__ == "__main__":
    app.run(debug=True)

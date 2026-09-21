from dash import Dash, Input, Output, State, dcc, html

from components import correlation, data_quality, distribution, overview, timeseries
from data_loader import get_sensor_columns, get_years, load_data
from filters import filter_data, format_summary

app = Dash(__name__)

df = load_data()
years = get_years(df)
sensor_columns = get_sensor_columns(df)

TAB_STYLE = {
    "padding": "14px 4px",
    "border": "none",
    "borderBottom": "2px solid transparent",
    "backgroundColor": "var(--bg)",
    "color": "var(--text-2)",
    "fontWeight": "500",
    "fontSize": "14px",
}
TAB_SELECTED_STYLE = {
    **TAB_STYLE,
    "borderBottom": "2px solid var(--co)",
    "color": "var(--text)",
    "fontWeight": "600",
}

SUN_ICON = html.Img(
    src=app.get_asset_url("icons/sun.svg"), className="icon-sun", alt=""
)
MOON_ICON = html.Img(
    src=app.get_asset_url("icons/moon.svg"), className="icon-moon", alt=""
)

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
        html.Div(
            [
                html.Div(
                    [
                        html.H3("필터"),
                        html.Label("연도 선택"),
                        dcc.Checklist(
                            id="year-filter",
                            options=[{"label": str(y), "value": y} for y in years],
                            value=years,
                        ),
                        html.Label("컬럼 선택"),
                        dcc.Checklist(
                            id="column-filter",
                            options=[{"label": c, "value": c} for c in sensor_columns],
                            value=sensor_columns,
                        ),
                    ],
                    className="sidebar",
                ),
                html.Div(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-overview",
                            className="app-tabs",
                            children=[
                                dcc.Tab(
                                    label="개요",
                                    value="tab-overview",
                                    style=TAB_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                ),
                                dcc.Tab(
                                    label="분포",
                                    value="tab-distribution",
                                    style=TAB_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                ),
                                dcc.Tab(
                                    label="시계열",
                                    value="tab-timeseries",
                                    style=TAB_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                ),
                                dcc.Tab(
                                    label="상관관계",
                                    value="tab-correlation",
                                    style=TAB_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                ),
                                dcc.Tab(
                                    label="데이터 품질",
                                    value="tab-quality",
                                    style=TAB_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                ),
                            ],
                        ),
                        html.Div(
                            id="tab-content",
                            children="준비 중",
                            className="content-card",
                        ),
                        html.Hr(),
                        html.Div(id="filter-summary", className="filter-summary"),
                    ],
                    className="main-panel",
                ),
            ],
            className="app-shell",
        ),
    ]
)


@app.callback(
    Output("filter-summary", "children"),
    Input("year-filter", "value"),
    Input("column-filter", "value"),
)
def update_filter_summary(selected_years, selected_columns):
    if not selected_years or not selected_columns:
        return "연도와 컬럼을 하나 이상 선택하세요."
    filtered = filter_data(df, selected_years, selected_columns)
    return format_summary(filtered, selected_years, selected_columns)


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("year-filter", "value"),
    Input("column-filter", "value"),
)
def update_tab_content(active_tab, selected_years, selected_columns):
    if not selected_years or not selected_columns:
        return "연도와 컬럼을 하나 이상 선택하세요."

    filtered = filter_data(df, selected_years, selected_columns)

    if active_tab == "tab-overview":
        return overview.render(filtered)
    if active_tab == "tab-distribution":
        return distribution.render(filtered)
    if active_tab == "tab-timeseries":
        return timeseries.render(filtered)
    if active_tab == "tab-correlation":
        return correlation.render(filtered)
    if active_tab == "tab-quality":
        return data_quality.render(filtered)
    return "준비 중"


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

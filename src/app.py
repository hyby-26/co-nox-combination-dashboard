from dash import Dash, Input, Output, dcc, html

from components import correlation, data_quality, distribution, overview, timeseries
from data_loader import get_sensor_columns, get_years, load_data
from filters import filter_data, format_summary

app = Dash(__name__)

df = load_data()
years = get_years(df)
sensor_columns = get_sensor_columns(df)

app.layout = html.Div(
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
            style={"width": "20%", "float": "left"},
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="tab-overview",
                    children=[
                        dcc.Tab(label="개요", value="tab-overview"),
                        dcc.Tab(label="분포", value="tab-distribution"),
                        dcc.Tab(label="시계열", value="tab-timeseries"),
                        dcc.Tab(label="상관관계", value="tab-correlation"),
                        dcc.Tab(label="데이터 품질", value="tab-quality"),
                    ],
                ),
                html.Div(id="tab-content", children="준비 중"),
                html.Hr(),
                html.Div(id="filter-summary"),
            ],
            style={"width": "75%", "float": "left"},
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


if __name__ == "__main__":
    app.run(debug=True)

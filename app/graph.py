from altair import Chart, Tooltip
from pandas import DataFrame

def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    properties = {
        "width": 600,
        "height": 400,
        "background": "#2a303c",
        "padding": 20,
    }

    graph = (
        Chart(df, title=f"{y} by {x} for {target}")
        .mark_circle(size=100)
        .encode(
            x=f"{x}:Q",
            y=f"{y}:Q",
            color=f"{target}:N",
            tooltip=Tooltip(df.columns.to_list())
        )
        .properties(**properties)
        .configure(
            axis={"labelColor": "#ffffff", "titleColor": "#ffffff"},
            title={"color": "#ffffff"},
            view={"stroke": "transparent"},
            background="#2a303c",
        )
    )

    return graph
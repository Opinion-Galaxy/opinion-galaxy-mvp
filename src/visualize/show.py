import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
from pandera.typing import DataFrame

from ..type import Dataset, Topics
from ..const import color_map

from .preprocess import (
    preprocess_basic_pie,
    preprocess_geo_scatter,
    preprocess_pie_by_sex,
    preprocess_radar_chart_by_sex,
    preprocess_time_series_area,
)


def visualize_basic_pie_chart(data: pd.DataFrame, selected_topic: Topics) -> None:
    data = preprocess_basic_pie(data, selected_topic)
    fig = px.pie(
        data,
        values="count",
        names=selected_topic,
        color=selected_topic,
        title=selected_topic + "についての意見",
        category_orders={selected_topic: ["賛成", "中立", "反対"]},
        color_discrete_map=color_map,
    )
    st.plotly_chart(fig, use_container_width=True)


def visualize_data_by_various_method(
    tabs, cumsum_radio_data: DataFrame[Dataset]
) -> None:
    with tabs[0]:
        fig = px.area(
            preprocess_time_series_area(cumsum_radio_data),
            y="cumsum",
            x="response_datetime",
            color="agree",  # , facet
            markers=True,
            color_discrete_map=color_map,
        )
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        fig = px.pie(
            preprocess_pie_by_sex(cumsum_radio_data),
            values="cumsum",
            names="agree",
            color="agree",
            title="賛成・反対の割合",
            facet_col="sex",
            category_orders={"agree": ["賛成", "中立", "反対"]},
            color_discrete_map=color_map,
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "polar"}, {"type": "polar"}]],
            subplot_titles=("男性", "女性"),
        )
        men_data, women_data = preprocess_radar_chart_by_sex(cumsum_radio_data)

        for i, d in enumerate([men_data, women_data]):
            radar = px.line_polar(
                d,
                r="cumsum",
                theta="age",
                color="agree",
                line_dash="sex",
                line_close=True,
                labels={"cumsum": "割合", "age": "年代", "agree": "賛成"},
                color_discrete_map=color_map,
                line_dash_map={"男性": "solid", "女性": "dot"},
            )
            for trace in radar.data:
                fig.add_trace(trace, row=1, col=i + 1)

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True),
                angularaxis=dict(showline=True, showticklabels=True),
            ),
            polar2=dict(
                radialaxis=dict(visible=True),
                angularaxis=dict(showline=True, showticklabels=True),
            ),
            legend=dict(
                orientation="v",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig.update_annotations(yshift=30)
        st.plotly_chart(fig, use_container_width=True)
        del men_data, women_data
    with tabs[3]:
        data = preprocess_geo_scatter(cumsum_radio_data)
        # Plotlyを使ってマップを描画
        fig = px.scatter_mapbox(
            data,
            lat="lat",
            lon="lon",
            color="cumsum",
            size="count",
            color_continuous_scale=px.colors.sequential.RdBu_r,
            size_max=15,
            zoom=3.5,
            mapbox_style="carto-positron",
            hover_name="address",
            width=360,
            height=540,
        )
        # Streamlitで表示
        st.plotly_chart(fig, use_container_width=True)

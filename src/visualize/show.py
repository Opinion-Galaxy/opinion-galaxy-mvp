import json
from typing import Tuple
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
from pandera.typing import DataFrame
import plotly.graph_objects as go
import geopandas as gpd

from ..type import Dataset, Topics
from ..const import color_map

from .preprocess import (
    preprocess_basic_pie,
    preprocess_geo_scatter,
    preprocess_pie_by_sex,
    preprocess_radar_chart_by_sex,
    preprocess_time_series_area,
)


@st.cache_data
def visualize_basic_pie_chart(data: pd.DataFrame, selected_topic: Topics) -> None:
    data = preprocess_basic_pie(data, selected_topic)
    fig = px.pie(
        data,
        values="count",
        names="value",
        color="value",
        category_orders={"value": ["賛成", "中立", "反対"]},
        color_discrete_map=color_map,
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def show_time_series_area(data: DataFrame[Dataset]) -> go.Figure:
    fig = px.area(
        preprocess_time_series_area(data),
        y="cumsum",
        x="response_datetime",
        color="agree",  # , facet
        markers=True,
        color_discrete_map=color_map,
        labels={"cumsum": "割合", "response_datetime": "日付", "agree": "意見"},
    )
    return fig


@st.cache_data
def show_pie_by_sex(data: DataFrame[Dataset]) -> go.Figure:
    fig = px.pie(
        preprocess_pie_by_sex(data),
        values="cumsum",
        names="agree",
        color="agree",
        title="賛成・反対の割合",
        facet_col="sex",
        category_orders={"agree": ["賛成", "中立", "反対"]},
        color_discrete_map=color_map,
    )
    return fig


@st.cache_data
def show_scatter_geo(data: DataFrame[Dataset]) -> go.Figure:
    geo = gpd.read_file("data/japan.geojson")
    geo["address"] = geo["N03_001"] + geo["N03_003"] + geo["N03_004"]
    geo = geo[["address", "N03_007"]]
    data = preprocess_geo_scatter(data)
    data = data.merge(geo, on="address", how="left")
    # Plotlyを使ってマップを描画
    fig = px.choropleth_map(
        data,
        geojson=json.load(open("data/japan.geojson")),
        locations="N03_007",
        featureidkey="properties.N03_007",
        # lat="lat",
        # lon="lon",
        color="cumsum",
        center={"lat": 36.531332, "lon": 137.151737},
        map_style="carto-positron",
        # size="count",
        color_continuous_scale=px.colors.cyclical.IceFire,
        # size_max=12,
        zoom=3.7,
        # mapbox_style="carto-positron",
        hover_name="address",
        width=360,
        height=540,
        range_color=[-1, 1],
    )

    return fig


@st.cache_data
def show_radar_chart(data: DataFrame[Dataset]) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "polar"}, {"type": "polar"}]],
        subplot_titles=("男性", "女性"),
    )
    men_data, women_data = preprocess_radar_chart_by_sex(data)

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

    del men_data, women_data
    return fig


async def visualize_data_by_various_method(
    tabs: Tuple[st._DeltaGenerator], cumsum_radio_data: DataFrame[Dataset]
) -> None:
    with tabs[0]:
        fig = show_time_series_area(cumsum_radio_data)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        fig = show_pie_by_sex(cumsum_radio_data)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        fig = show_radar_chart(cumsum_radio_data)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        fig = show_scatter_geo(cumsum_radio_data)
        # Streamlitで表示
        st.plotly_chart(fig, use_container_width=True)

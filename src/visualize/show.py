import base64
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from typing import Tuple
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
from pandera.typing import DataFrame
import plotly.graph_objects as go
import geopandas as gpd
from PIL import Image

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
    fig.update_layout(
       font=dict(size=18, weight="bold"),
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
    fig.update_layout(
       font=dict(size=20, weight="bold"),
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
    fig.update_layout(
       font=dict(size=18, weight="bold"),
    )
    return fig


# def b64image(df):
#     fig = px.bar(
#         df,
#         y="cumsum",
#         color="agree",
#         template="plotly",
#         color_discrete_map=color_map
#     ).update_layout(
#         showlegend=False,
#         xaxis_visible=False,
#         yaxis_visible=False,
#         bargap=0,
#         margin={"l": 0, "r": 0, "t": 0, "b": 0},
#         autosize=False,
#         height=100,
#         width=100,
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#     )
#     fig.update_traces(width=0.6)
#     b = BytesIO(fig.to_image(format="png", scale=2))
#     b64 = base64.b64encode(b.getvalue())
#     return "data:image/png;base64," + b64.decode("utf-8")

# # Sample data structure

# def process_group(group_tuple):
#     group, df = group_tuple
#     # Generate the base64-encoded image
#     encoded_image = b64image(df.copy())
    
#     # Calculate centroid buffer and envelope
#     centroid = df.iloc[0]["geometry"].centroid
#     buffered = centroid.buffer(1.1)
#     envelope = buffered.envelope
#     exterior_coords = list(envelope.exterior.coords)
    
#     # Prepare coordinates as per Mapbox requirement
#     coordinates = [list(coord) for coord in exterior_coords[:-1]][::-1]
    
#     return {
#         "sourcetype": "image",
#         "source": encoded_image,
#         "coordinates": coordinates,
#     }

# def create_multithreaded_dicts(data):
#     # Group the data by 'prefecture'
#     grouped = data.groupby("prefecture")
    
#     # Convert groupby object to list of tuples for multiprocessing
#     group_tuples = list(grouped)
    
#     # Use ProcessPoolExecutor for CPU-bound tasks
#     with ThreadPoolExecutor(max_workers=6) as executor:
#         # Map the process_group function to each group
#         results = list(executor.map(process_group, group_tuples))
    
#     return results

@st.cache_data
def show_scatter_geo(data: DataFrame[Dataset], geojoson_path = "data/prefectures.geojson") -> go.Figure:
    geo = gpd.read_file(geojoson_path).rename({"N03_001": "prefecture"}, axis=1)
    # print(geo)
    # geo["address"] = geo["N03_001"] + geo["N03_003"] + geo["N03_004"]
    # geo = geo[["address", "N03_007"]]
    data = preprocess_geo_scatter(data)
    data = gpd.GeoDataFrame(data.merge(geo, on="prefecture", how="left"))
    abs_max = max(abs(data["cumsum"]))
    # Plotlyを使ってマップを描画
    geojson = json.load(open(geojoson_path))
    fig = px.choropleth_map(
        data,
        geojson=geojson,
        locations="prefecture",
        featureidkey="properties.prefecture",
        # lat="lat",
        # lon="lon",
        color="cumsum",
        center={"lat": 36.531332, "lon": 137.151737},
        map_style="carto-positron",
        color_continuous_scale=px.colors.diverging.RdYlBu_r,
        zoom=3.7,
        hover_name="prefecture",
        width=360,
        height=540,
        range_color=[0.1, 0.9],
    )
    fig.update_layout(
       font=dict(size=16, weight="bold"),
       margin={"l": 0, "r": 0, "t": 0, "b": 0},
       coloraxis_colorbar=dict(len=0.55, title=dict(text="賛成割合", font_color="black"), x=0, y=0.67, ticks="inside", tickfont=dict(size=15, color="black")),
    )

    # fig = px.choropleth_mapbox(
    #     data,
    #     geojson=geojson,
    #     locations="prefecture",
    #     featureidkey="properties.prefecture",
    #     color_discrete_sequence=["lightgrey"],
    # )
    # fig.update_layout(
    #     margin={"l": 0, "r": 0, "t": 0, "b": 0},
    #     showlegend=False,
    #     mapbox=dict(
    #         style="carto-positron",
    #         center={"lat": 36.531332, "lon": 137.151737},
    #         zoom=3.7,
    #         layers=create_multithreaded_dicts(data),
    #         pitch=60
    #     )
    # )
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
            radialaxis=dict(visible=True, color="black"),
            angularaxis=dict(showline=True, showticklabels=True),
        ),
        polar2=dict(
            radialaxis=dict(visible=True, color="black"),
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



def visualize_data_by_various_method(
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

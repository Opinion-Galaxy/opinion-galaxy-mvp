import streamlit as st
import plotly.express as px
import pandas as pd

opinion_map = {"1": "賛成", "0": "中立", "-1": "反対"}

color_map = {
    "賛成": px.colors.sequential.RdBu_r[2],
    "中立": px.colors.sequential.RdBu_r[4],
    "反対": px.colors.sequential.RdBu_r[-3],
}

figure_tabs = ["意見の推移", "性別の割合", "性別・年代別の割合", "地域別の賛成割合"]


@st.cache_data
def get_prefecture_city():
    prefecture_city = pd.read_csv(
        "data/prefecture_city_lonlat.csv",
        encoding="utf-8",
    )
    return prefecture_city


# @st.cache_data
def get_prefecture_and_city_list():
    prefecture_city = get_prefecture_city()
    return (
        prefecture_city["都道府県名"].unique().tolist(),
        prefecture_city.groupby("都道府県名")["市区町村名"].unique().to_dict(),
    )


prefecture_list, city_dict = get_prefecture_and_city_list()
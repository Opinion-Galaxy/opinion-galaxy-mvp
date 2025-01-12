import streamlit as st
import plotly.express as px
import pandas as pd

# 論点リスト
topics = [
    "外国人労働者の受け入れ拡大",
    "子育て支援の充実",
    "インフラ投資の強化",
    "イノベーションの促進",
    "防衛力の強化",
    "憲法９条の改正",
    "再生可能エネルギーの導入促進",
    "エネルギー安全保障の確保",
    "日米同盟の廃止",
    "教育格差の是正",
    "地域資源の活用",
    "働き方の多様化",
    "労働法制の整備",
    "在宅医療の推進",
    "介護人材の確保",
    "医療費の持続可能性確保",
    "サイバーセキュリティの強化",
    "電子政府（e-Government）の推進",
]

opinion_map = {"-1": "反対", "0": "中立", "1": "賛成"}

color_map = {
    "反対": px.colors.sequential.RdBu_r[-3],
    "中立": px.colors.sequential.RdBu_r[4],
    "賛成": px.colors.sequential.RdBu_r[2],
}

figure_tabs = ["意見の推移", "性別の割合", "性別・年代別の割合", "地域別の賛成割合"]


@st.cache_data
def get_prefecture_city():
    prefecture_city = pd.read_csv(
        "data/prefecture_city_lonlat.csv",
        encoding="utf-8",
    )
    return prefecture_city


@st.cache_data
def get_prefecture_and_city_list():
    prefecture_city = get_prefecture_city()
    return (
        prefecture_city["都道府県名"].unique().tolist(),
        prefecture_city.groupby("都道府県名")["市区町村名"].unique().to_dict(),
    )


prefecture_list, city_dict = get_prefecture_and_city_list()

button_style = """
    <style>
    div.st-key-opinion-container div.stColumn:nth-of-type(1) div.stButton > button:first-child {
        background-color: rgb(67, 147, 195);
        color: black;
    }
    div.st-key-opinion-container div.stColumn:nth-of-type(2) div.stButton > button:first-child {
        background-color: rgb(209, 229, 240);
        color: black;
    }
    div.st-key-opinion-container div.stColumn:nth-of-type(3) div.stButton > button:first-child {
        background-color: rgb(214, 96, 77);
        color: black;
    }
    div.st-key-opinion-container div.stColumn {
        min-width: 60px;
        justify-content: center;
        align-content: center;
    }
    </style>
"""

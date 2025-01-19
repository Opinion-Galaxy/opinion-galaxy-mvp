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

japanese_names = [
    "佐藤太郎",
    "鈴木花子",
    "高橋健一",
    "田中美咲",
    "伊藤翔",
    "渡辺愛",
    "山本大輔",
    "中村絵里",
    "小林悠",
    "加藤優子",
    "吉田一郎",
    "山田菜々子",
    "佐々木悠斗",
    "山口彩",
    "松本健太",
    "井上葵",
    "木村龍之介",
    "林美咲",
    "斎藤翔太",
    "清水結衣",
    "山崎健",
    "森田真奈",
    "阿部翔",
    "池田美穂",
    "橋本拓海",
    "石川葵",
    "山下大地",
    "松井葵",
    "中島翔子",
    "石井健",
    "藤田美香",
    "木下翔",
    "村上優子",
    "原田一郎",
    "長谷川葵",
    "小川健太",
    "西村美咲",
    "岡田翔太",
    "藤井彩",
    "田村大輔",
    "松田美穂",
    "菅原翔",
    "山口真奈",
    "坂本健",
    "大野葵",
    "上田悠",
    "森健一",
    "小山菜々子",
    "石橋翔太",
    "石田葵",
]

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

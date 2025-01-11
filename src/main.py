import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from pygwalker.api.streamlit import StreamlitRenderer
import plotly.graph_objects as go

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# サイドバーの作成
st.sidebar.header("政治論点メニュー")

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
# ユーザーが選択した論点
selected_topic = st.sidebar.selectbox("論点を選択してください", topics)

topics_idx = topics.index(selected_topic)

st.header(selected_topic)


def show_topic_info():
    st.write("選択された論点に関する情報を表示します。")


def plot_peichart():
    pass


# サンプルデータの作成
@st.cache_data
def load_data():
    data = pd.read_csv(
        "data/dummy_political_opinions_with_datetime.csv",
        parse_dates=["response_datetime"],
        converters={topic: lambda x: opinion_map[x] for topic in topics},
    ).sort_values("response_datetime")
    data["age"] = pd.cut(
        data["age"],
        np.arange(10, 100, 10),
        labels=np.arange(10, 90, 10).astype(str).astype(object) + "代",
    )

    data["response_datetime"] = data["response_datetime"].dt.strftime("%Y-%m-%d")
    return data


data = load_data()


def create_dataset(selected_topic, agree_neutral_disagree="賛成"):
    selected_data = data[data[selected_topic] == agree_neutral_disagree].copy()
    cumsum_data = (
        selected_data.groupby(["sex", "age", "response_datetime", "address"])[
            selected_topic
        ]
        .count()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum(axis=1)
    )

    cumsum_radio_data = cumsum_data.div(
        data.groupby(["sex", "age", "response_datetime", "address"])[selected_topic]
        .count()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum(axis=1),
        axis=0,
    )
    cumsum_radio_data["agree"] = agree_neutral_disagree
    return cumsum_radio_data


fig = px.pie(
    pd.DataFrame(data[selected_topic].value_counts()).reset_index(),
    values="count",
    names=selected_topic,
    color=selected_topic,
    title=selected_topic + "についての意見",
    category_orders={selected_topic: ["賛成", "中立", "反対"]},
    color_discrete_map=color_map,
)
st.plotly_chart(fig, use_container_width=True)

tabs = st.tabs(["意見の推移", "性別の割合", "性別・年代別の割合", "地域別の賛成割合"])
# data["hour"] = data["response_datetime"].dt.hour

cumsum_radio_data = (
    pd.concat([create_dataset(selected_topic, i) for i in opinion_map.values()])
    .melt(ignore_index=False, value_name="cumsum", id_vars=["agree"])
    .reset_index()
)

with tabs[0]:
    fig = px.area(
        cumsum_radio_data.groupby(["response_datetime", "agree"])["cumsum"]
        .mean()
        .reset_index(),
        y="cumsum",
        x="response_datetime",
        color="agree",  # , facet
        markers=True,
        color_discrete_map=color_map,
    )
    st.plotly_chart(fig, use_container_width=True)
with tabs[1]:
    print(cumsum_radio_data)
    fig = px.pie(
        cumsum_radio_data,
        values="cumsum",
        names="agree",
        color="agree",
        title="賛成・反対の割合",
        facet_col="sex",
        category_orders={"agree": ["賛成", "中立", "反対"]},
        color_discrete_map=color_map,
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def merge_lonlat(data):
    prefecture_city = pd.read_csv(
        "data/prefecture_city_lonlat.csv",
        encoding="utf-8",
    )
    prefecture_city["address"] = (
        prefecture_city["都道府県名"] + prefecture_city["市区町村名"]
    )
    prefecture_city_lonlat = (
        prefecture_city.groupby(["address"])[["緯度", "経度"]]
        .mean()
        .reset_index()
        .rename(columns={"緯度": "lat", "経度": "lon"})
    )
    data = data.merge(
        prefecture_city_lonlat, how="left", left_on="address", right_on="address"
    )
    del prefecture_city, prefecture_city_lonlat
    return data


with tabs[2]:
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "polar"}, {"type": "polar"}]],
        subplot_titles=("男性", "女性"),
    )
    data_by_sex_age = (
        cumsum_radio_data.groupby(["sex", "age", "agree"])["cumsum"]
        .mean()
        .reset_index()
    )
    men_data = data_by_sex_age[data_by_sex_age["sex"] == "男性"]
    women_data = data_by_sex_age[data_by_sex_age["sex"] == "女性"]
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
    del men_data, women_data, data_by_sex_age
with tabs[3]:
    print(cumsum_radio_data)
    count = (
        cumsum_radio_data.dropna(subset="cumsum", how="any")
        .groupby("address")["agree"]
        .count()
        .rename("count")
        .reset_index()
    )
    cumsum_radio_data.loc[cumsum_radio_data["agree"] == "反対", "cumsum"] *= -1
    cumsum_radio_data_by_city = (
        cumsum_radio_data.groupby("address")["cumsum"].mean().reset_index()
    )
    cumsum_radio_data = cumsum_radio_data_by_city.merge(count, how="left", on="address")
    data = merge_lonlat(cumsum_radio_data)
    del cumsum_radio_data
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
# pyg_app = StreamlitRenderer(
#     cumsum_radio_data.reset_index()[["sex", "agree", "cumsum", "response_datetime"]],
# )
# pyg_app.explorer()

# フッター
st.markdown("---")
st.write("© 2025 Opinion Galaxy Inc.")

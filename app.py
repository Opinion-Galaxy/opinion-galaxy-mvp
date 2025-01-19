import asyncio
import sqlite3
import pandas as pd
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.visualize.show import (
    show_pie_by_sex,
    show_radar_chart,
    show_scatter_geo,
    show_time_series_area,
)

from src.visualize import (
    visualize_basic_pie_chart,
)
from src.type import Topics
from src.data import load_data, create_dataset
from src.api import driver, usecase
from src.components import (
    comment_container,
    comment_wrapper_style,
    opinion_info,
    basic_info_dialog,
    select_opinion_container,
    select_opinion_style,
    visualize_tabs,
)

pd.set_option("display.max_columns", 100)


# -------------------
# Cached Database Connection
# -------------------
@st.cache_resource
def get_db_connection(db_path="data/database.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------
# Cached Class Instances
# -------------------
@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_user_driver_instance(conn: sqlite3.Connection):
    return driver.User(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_comment_driver_instance(conn):
    return driver.Comment(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_answer_driver_instance(conn):
    return driver.Answer(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_topic_instance(conn):
    return driver.Topic(conn)


# Initialize cached resources
conn = get_db_connection()

user_driver, comment_driver, answer_driver, topic_driver = (
    get_user_driver_instance(conn),
    get_comment_driver_instance(conn),
    get_answer_driver_instance(conn),
    get_topic_instance(conn),
)


@st.cache_resource(hash_funcs={driver.Comment: lambda x: len(x.get_all())})
def get_comment_usecace_instance():
    return usecase.Comment(comment_driver)


usecase_user, usecase_comment, usecase_answer = (
    usecase.User(user_driver),
    usecase.Comment(comment_driver),
    usecase.Answer(answer_driver),
)


topics = [row["topic"] for row in topic_driver.get_all()]

if "add_new_data" in st.session_state and st.session_state.add_new_data:
    load_data.clear()
    create_dataset.clear()
    show_time_series_area.clear()
    show_pie_by_sex.clear()
    show_radar_chart.clear()
    show_scatter_geo.clear()
    visualize_basic_pie_chart.clear()
    opinion_info.clear()
    st.session_state.add_new_data = False

data = load_data(usecase_answer, usecase_user)

# サイドバーの作成
st.sidebar.header("政治論点メニュー")

# ユーザーが選択した論点
selected_topic: Topics = st.sidebar.selectbox("論点を選択してください", topics)

################################
# ユーザー基本情報
################################


def open_basic_info_dialog(usecase_user):
    def _open_basic_info_dialog():
        basic_info_dialog(usecase_user)

    return _open_basic_info_dialog


basic_info_button = st.sidebar.button(
    "基本情報を変更する",
    key="basic-info-button",
)
# ユーザー情報の変更
if basic_info_button or (
    "basic_info_button" in st.session_state and st.session_state.basic_info_button
):
    basic_info_dialog(usecase_user)
    st.session_state.basic_info_button = False

# ユーザー情報の初期画面
if "basic_info" not in st.session_state:
    basic_info_dialog(usecase_user)
    st.stop()

topics_idx = topics.index(selected_topic)

st.header(selected_topic)


################################
# データの可視化
################################
@st.fragment
async def visualize():
    # ---------------------
    # 投票数の表示
    # ---------------------
    opinion_info(data, selected_topic)

    # ---------------------
    # 意見の可視化
    # ---------------------
    await visualize_tabs(data, selected_topic)

    # ---------------------
    # 意見の投稿
    # ---------------------
    st.markdown(
        select_opinion_style,
        unsafe_allow_html=True,
    )


    await select_opinion_container(usecase_answer, selected_topic, topics_idx)

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
loop.run_until_complete(visualize())

# ---------------------
# コメントの投稿
# ---------------------
st.markdown(comment_wrapper_style, unsafe_allow_html=True)

st.header("コメント")
comment_container(usecase_comment, usecase_user, topics_idx)


st.markdown("---")
st.write("© 2025 Opinion Galaxy Inc.")

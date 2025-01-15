import pandas as pd
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.visualize import (
    visualize_basic_pie_chart,
    visualize_data_by_various_method,
)
from src.type import Topics
from src.data import (
    load_data,
    create_dataset,
    merge_lonlat,
)
from src.api import driver, usecase
from src.components import (
    comment_container,
    comment_container_style,
    opinion_info,
    basic_info_dialog,
    select_opinion_container,
    select_opinion_style,
    visualize_tabs,
)

pd.set_option("display.max_columns", 100)


@st.cache_resource
def get_comment_instance():
    return usecase.Comment(driver)


@st.cache_resource
def get_user_instance():
    return usecase.User(driver)


@st.cache_resource
def get_answer_instance():
    return usecase.Answer(driver)


usecase_comment = get_comment_instance()
usecase_user = get_user_instance()
usecase_answer = get_answer_instance()

topic_driver = driver.Topic()
topics = topic_driver.get_all()["topic"].tolist()


if "add_new_data" in st.session_state and st.session_state.add_new_data:
    load_data.clear()
    create_dataset.clear()
    merge_lonlat.clear()
    visualize_data_by_various_method.clear()
    visualize_basic_pie_chart.clear()
    opinion_info.clear()
    st.session_state.add_new_data = False

data = load_data(usecase_answer, usecase_user)

if "basic_info" not in st.session_state:
    basic_info_dialog(usecase_user)

# サイドバーの作成
st.sidebar.header("政治論点メニュー")


def open_basic_info_dialog(usecase_user):
    def _open_basic_info_dialog():
        basic_info_dialog(usecase_user)

    return _open_basic_info_dialog


# ユーザーが選択した論点
selected_topic: Topics = st.sidebar.selectbox("論点を選択してください", topics)
st.sidebar.button(
    "基本情報を変更する",
    key="basic-info-button",
)

if "basic_info_button" in st.session_state and st.session_state.basic_info_button:
    basic_info_dialog(usecase_user)
    st.session_state.basic_info_button = False

topics_idx = topics.index(selected_topic)

st.header(selected_topic)
# ---------------------
# 投票数の表示
# ---------------------
opinion_info(data, selected_topic)

# ---------------------
# 意見の可視化
# ---------------------
visualize_tabs(data, selected_topic)


# ---------------------
# 意見の投稿
# ---------------------
st.markdown(
    select_opinion_style,
    unsafe_allow_html=True,
)
select_opinion_container(usecase_answer, selected_topic, topics_idx)

# ---------------------
# コメントの投稿
# ---------------------
st.markdown(comment_container_style, unsafe_allow_html=True)

comment_container(usecase_comment, usecase_user, topics_idx)


st.markdown("---")
st.write("© 2025 Opinion Galaxy Inc.")

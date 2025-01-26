import streamlit as st

from src.api import usecase

from src.database import get_db_connection, get_user_driver_instance, get_comment_driver_instance, get_answer_driver_instance
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
from src.components import (
    comment_container,
    comment_wrapper_style,
    opinion_info,
    select_opinion_container,
    select_opinion_style,
    share_container,
    visualize_tabs,
)

@st.fragment
def visualize(data, selected_topic, usecase_answer, topics_idx):
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


def generate_page(selected_topic, usecase_user, usecase_comment, usecase_answer):
    print(selected_topic)
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

    topics_idx = st.session_state.topics.index(selected_topic)

    st.header(selected_topic)
    ################################
    # データの可視化
    ################################


    visualize(data, selected_topic, usecase_answer, topics_idx)

    share_container(selected_topic)
    # ---------------------
    # コメントの投稿
    # ---------------------
    st.markdown(comment_wrapper_style, unsafe_allow_html=True)

    st.subheader("コメント")
    comment_container(usecase_comment, usecase_user, topics_idx)


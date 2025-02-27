import streamlit as st

from src.visualize.show import (
    show_pie_by_sex,
    show_radar_chart,
    show_scatter_geo,
    show_time_series_area,
)

from src.visualize import (
    visualize_basic_pie_chart,
)
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
def visualize(selected_topic, usecase_user, usecase_answer, topics_idx):
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
    topics_idx = st.session_state.topics.index(selected_topic)

    st.header(selected_topic, anchor=selected_topic)
    ################################
    # データの可視化
    ################################

    visualize(selected_topic, usecase_user, usecase_answer, topics_idx)

    share_container(selected_topic)
    # ---------------------
    # コメントの投稿
    # ---------------------
    st.markdown(comment_wrapper_style, unsafe_allow_html=True)

    st.subheader("コメント")
    comment_container(usecase_comment, usecase_user, topics_idx)

    # st.markdown(f'''
    #             <link rel="stylesheet" rel="preload" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=home" />
    #             <style>
    #                 .back_to_dashboard {{
    #                     position: fixed;
    #                     bottom: 3vh;
    #                     right: 15px;
    #                 }}
    #                 .back_to_dashboard button {{
    #                     color: white;
    #                     text-align: center;
    #                     padding: 4px 8px;
    #                     text-decoration: none;
    #                     display: inline-block;
    #                     font-size: 13px;
    #                     margin: 4px 2px;
    #                     border-radius: 16px;
    #                     cursor: pointer;
    #                     background-color: #ff4b4b;
    #                     letter-spacing: -1px;
    #                 }}
    #                 .material-symbols-outlined {{
    #                     font-variation-settings:
    #                     'FILL' 0,
    #                     'wght' 400,
    #                     'GRAD' 0,
    #                     'opsz' 24
    #                 }}
    #                 a[href*="https://streamlit.io/cloud"], a[href*="https://share.streamlit.io"] {{
    #                     display: none;
    #                 }}
    #             </style>
    #             <a target="_self" href="#" class="back_to_dashboard" kind="primary">
    #                 <button>
    #                     <span class="material-symbols-outlined">home</span>
    #                 </button>
    #             </a>''', unsafe_allow_html=True)

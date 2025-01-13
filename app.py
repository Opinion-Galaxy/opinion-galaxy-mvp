import pandas as pd
import streamlit as st


from src.visualize import (
    visualize_basic_pie_chart,
    visualize_data_by_various_method,
)
from src.type import Topics
from src.data import (
    load_data,
    create_dataset,
    check_same_data,
    add_new_data,
    merge_lonlat,
)
from src.const import (
    topics,
    opinion_map,
    figure_tabs,
    prefecture_list,
    city_dict,
    button_style,
)


@st.cache_data
def show_opinion_nums(data, selected_topic):
    opinion_nums = data[selected_topic].value_counts()
    st.write("投票数", opinion_nums.sum())
    cols = st.columns(3)
    for i, (key, num) in enumerate(opinion_nums.to_dict().items()):
        with cols[i]:
            st.write(key, num)


# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "add_new_data" in st.session_state and st.session_state.add_new_data:
    load_data.clear()
    create_dataset.clear()
    merge_lonlat.clear()
    # visualize_data_by_various_method.clear()
    visualize_basic_pie_chart.clear()
    show_opinion_nums.clear()

data = load_data()


@st.dialog("基本情報の入力")
def input_basic_info():
    age = st.number_input("年齢", min_value=0, max_value=100, value=30)
    sex = st.radio(
        "性別",
        ["女性", "男性"],
        horizontal=True,
    )
    prefecture = st.selectbox("都道府県", prefecture_list, index=12)
    city = st.selectbox("市区町村", city_dict[prefecture])
    if st.button("送信"):
        st.session_state.basic_info = {
            "age": age,
            "sex": sex,
            "address": prefecture + city,
        }
        st.rerun()


if "basic_info" not in st.session_state:
    input_basic_info()

# サイドバーの作成
st.sidebar.header("政治論点メニュー")

# ユーザーが選択した論点
selected_topic: Topics = st.sidebar.selectbox("論点を選択してください", topics)

topics_idx = topics.index(selected_topic)


st.header(selected_topic)


with st.container(border=True, key="opinion-values-container"):
    show_opinion_nums(data, selected_topic)
    visualize_basic_pie_chart(data, selected_topic)

tabs = st.tabs(figure_tabs)

cumsum_radio_data = create_dataset(data, selected_topic)

visualize_data_by_various_method(tabs, cumsum_radio_data)


st.markdown(
    button_style,
    unsafe_allow_html=True,
)

with st.container(border=True, key="select-opinion-container"):
    cols = st.columns(3, vertical_alignment="center", gap="medium")
    with cols[0]:
        agree = st.button("賛成", use_container_width=True)
    with cols[1]:
        neutral = st.button("中立", use_container_width=True)
    with cols[2]:
        disagree = st.button("反対", use_container_width=True)

if any([agree, neutral, disagree]):
    original = pd.read_csv(
        "data/dummy_political_opinions_with_datetime.csv",
        parse_dates=["response_datetime"],
    ).sort_values("response_datetime")
    age = st.session_state.basic_info["age"]
    sex = st.session_state.basic_info["sex"]
    address = st.session_state.basic_info["address"]
    same_data = check_same_data(
        original, selected_topic, agree, disagree, age, sex, address
    )
    add_new_data(
        original, same_data, selected_topic, agree, disagree, age, sex, address
    )
    del data
    st.session_state.add_new_data = True
    st.rerun()

# フッター
st.markdown("---")
st.write("© 2025 Opinion Galaxy Inc.")

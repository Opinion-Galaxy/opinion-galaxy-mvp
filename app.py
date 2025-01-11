import streamlit as st


from src.visualize import (
    visualize_basic_pie_chart,
    visualize_data_by_various_method,
)
from src.type import Topics
from src.data import load_data, create_dataset
from src.const import topics, opinion_map, figure_tabs

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# サイドバーの作成
st.sidebar.header("政治論点メニュー")

data = load_data()

# ユーザーが選択した論点
selected_topic: Topics = st.sidebar.selectbox("論点を選択してください", topics)

topics_idx = topics.index(selected_topic)

st.header(selected_topic)

visualize_basic_pie_chart(data, selected_topic)

tabs = st.tabs(figure_tabs)

cumsum_radio_data = create_dataset(data, selected_topic, opinion_map)

visualize_data_by_various_method(tabs, cumsum_radio_data)

# pyg_app = StreamlitRenderer(
#     cumsum_radio_data.reset_index()[["sex", "agree", "cumsum", "response_datetime"]],
# )
# pyg_app.explorer()

# フッター
st.markdown("---")
st.write("© 2025 Opinion Galaxy Inc.")

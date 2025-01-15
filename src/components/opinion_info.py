import streamlit as st
from src.visualize import visualize_basic_pie_chart


@st.cache_data
def opinion_info(data, selected_topic):
    with st.container(border=True, key="opinion-values-container"):
        opinion_order = ["賛成", "中立", "反対"]
        sorter_index = dict(zip(opinion_order, range(len(opinion_order))))
        opinion_nums = (
            data.loc[data["topic"] == selected_topic, "value"]
            .value_counts()
            .sort_index(key=lambda x: x.map(sorter_index))
        )
        st.write("投票数", opinion_nums.sum())
        cols = st.columns(3)
        for i, (key, num) in enumerate(opinion_nums.to_dict().items()):
            with cols[i]:
                st.metric(key, num)

        visualize_basic_pie_chart(data, selected_topic)

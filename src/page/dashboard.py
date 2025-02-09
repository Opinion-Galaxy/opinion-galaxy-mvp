from datetime import datetime, timedelta
import streamlit as st

from src.data import load_data

dashboard_style = """
<style>
    div:has(> div[class*='st-key-dashboard-container-']){
        width: 100%;
    }
    div[class*='st-key-dashboard-container-'] {
        width: 100%;
    }
    div[data-testid='stVerticalBlockBorderWrapper']:has(>div > div[class*='st-key-dashboard-container-']) {
        min-height: 158px;
    }
    div[data-testid='stVerticalBlockBorderWrapper']:has(div[class*='st-key-dashboard-container-']) > div {
        width: 100%;
    }
    .stHorizontalBlock:has(div[class*='st-key-dashboard-container-']) {
        gap: 0.5rem;
    }
    .stColumn:has(div[class*='st-key-dashboard-container-']) {
        width: calc(50% - 0.5rem);
    }
    div[class*='st-key-dashboard-container-'] p{
        font-size: 0.9rem;
    }
    .stColumn:has(div[class*='st-key-dashboard-container-']) > div {
        width: 100%;
    }
    div[class*='danger'] div.stElementContainer div[data-testid='stMetricValue'] > div {
        color: rgb(214 96 76);
    }
    div[class*='clear']  div.stElementContainer div[data-testid='stMetricValue'] > div {
        color: #4393c3;
    }
    div[class*='st-key-dashboard-container-'] div.stPageLink a {
        padding: 0;
    }
    div[class*='st-key-dashboard-container-'] div.stPageLink a p{
        white-space: break-spaces;
        line-height: 1.4;
    }
</style>
"""


def dashboard(topics, pages, usecase_answer, usecase_user):
    st.markdown(dashboard_style, unsafe_allow_html=True)
    st.header("ダッシュボード")
    data = load_data(usecase_answer, usecase_user)
    d_by_topic = []
    for topic in topics:
        d = data[data["topic"] == topic]
        if len(d_by_topic) == 0:
            d_by_topic.append((d,))
            continue
        last = d_by_topic[-1]
        if len(last) == 1:
            d_by_topic[-1] = (last[0], d)
        else:
            d_by_topic.append((d,))
    for i, (first_d, second_d) in enumerate(d_by_topic):
        cols = st.columns(2)
        if first_d is not None:
            with cols[0]:
                topic = first_d["topic"].iloc[0]
                topic_id = topics.index(topic)
                prev_first_d = first_d[
                    first_d["response_datetime"]
                    < (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                ]
                prev_first_rate = (
                    round(
                        (prev_first_d["value"] == "賛成").sum() / len(prev_first_d), 3
                    )
                    * 100
                )
                agree_rate = (
                    round((first_d["value"] == "賛成").sum() / len(first_d), 3) * 100
                )
                if agree_rate < 40:
                    label = "danger"
                elif agree_rate > 60:
                    label = "clear"
                else:
                    label = " normal"
                with st.container(
                    border=True, key=f"dashboard-container-{topic_id}-{label}"
                ):
                    st.page_link(pages[i * 2], label=topic)
                    st.metric(
                        "賛成率",
                        f"{round((first_d['value'] == '賛成').sum() / len(first_d), 3) * 100:.1f}"
                        "%",
                        f"{agree_rate - prev_first_rate:.1f}%",
                    )
        if second_d is not None:
            with cols[1]:
                topic = second_d["topic"].iloc[0]
                topic_id = topics.index(topic)
                prev_second_d = second_d[
                    second_d["response_datetime"]
                    < (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                ]
                prev_second_rate = (
                    round(
                        (prev_second_d["value"] == "賛成").sum() / len(prev_second_d), 3
                    )
                    * 100
                )
                agree_rate = (
                    round((second_d["value"] == "賛成").sum() / len(second_d), 3) * 100
                )
                if agree_rate < 50:
                    label = "danger"
                elif agree_rate < 70:
                    label = "normal"
                else:
                    label = "clear"
                with st.container(
                    border=True, key=f"dashboard-container-{topic_id}-{label}"
                ):
                    st.page_link(pages[i * 2 + 1], label=topic)
                    st.metric(
                        "賛成率",
                        f"{round((second_d['value'] == '賛成').sum() / len(second_d), 3) * 100:.1f}"
                        "%",
                        f"{agree_rate - prev_second_rate:.1f}%",
                    )
    st.divider()
    st.write("※前週比は前週の賛成率とこれまでの賛成率の差を表しています")

import streamlit as st


select_opinion_style = """
    <style>
    div.st-key-select-opinion-container div.stColumn:nth-of-type(1) div.stButton > button:first-child {
        background-color: rgb(67, 147, 195);
        color: black;
    }
    div.st-key-select-opinion-container div.stColumn:nth-of-type(2) div.stButton > button:first-child {
        background-color: rgb(209, 229, 240);
        color: black;
    }
    div.st-key-select-opinion-container div.stColumn:nth-of-type(3) div.stButton > button:first-child {
        background-color: rgb(214, 96, 77);
        color: black;
    }
    div.st-key-select-opinion-container div.stColumn {
        min-width: 60px;
        justify-content: center;
        align-content: center;
    }
    </style>
"""


def select_opinion_container(usecase_answer, selected_topic, topics_idx):
    with st.container(border=True, key="select-opinion-container"):
        cols = st.columns(3, vertical_alignment="center", gap="medium")
        with cols[0]:
            agree = st.button("賛成", use_container_width=True)
        with cols[1]:
            neutral = st.button("中立", use_container_width=True)
        with cols[2]:
            disagree = st.button("反対", use_container_width=True)

    if any([agree, neutral, disagree]):
        user_id = st.session_state.basic_info["user_id"]
        user_answers = usecase_answer.get_user_answers(user_id)
        value = 1 if agree else 0 if neutral else -1
        if user_answers[user_answers["topic_id"] == selected_topic].empty:
            usecase_answer.create_answer(user_id, topics_idx + 1, value)
        else:
            id = user_answers.loc[
                user_answers["topic_id"] == selected_topic, "id"
            ].values[0]
            usecase_answer.update_answer(id, value)
        st.session_state.add_new_data = True
        st.rerun()

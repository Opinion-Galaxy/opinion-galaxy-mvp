import streamlit as st
from time import sleep
import logging

logger = logging.getLogger(__name__)


def on_submitted(id, is_agree):
    st.session_state[f"submitted-{id}"] = True
    st.session_state[f"agreed-{id}"] = is_agree



def reset_submitted(id):
    st.session_state[f"submitted-{id}"] = False
    st.session_state.comment_fragment_rerun = True


def reaction_columns(id, favorite_count, bad_count, usecase_comment, topics_idx):
    reaction_cols = st.columns(4, vertical_alignment="center")
    with reaction_cols[0]:
        agreed = st.button(
            "賛同", key=f"agree_{id}", icon="👍",
            on_click=lambda: reset_submitted(id)
        )
    with reaction_cols[1]:
        disagreed = st.button(
            "反論", key=f"disagree_{id}", icon="👎",
            on_click=lambda: reset_submitted(id)
        )
    with reaction_cols[2]:
        favorited = st.button(
            str(favorite_count),
            key=f"favorite_{id}",
            icon=":material/favorite:",
            on_click=lambda: usecase_comment.get_comments_at_topic.clear(),
        )
    with reaction_cols[3]:
        baded = st.button(
            str(bad_count),
            key=f"bad_{id}",
            icon=":material/close:",
            on_click=lambda: usecase_comment.get_comments_at_topic.clear(),
        )

    if f"successed-comment-{id}" in st.session_state:
        print(f"successed-comment-{id}", st.session_state[f"successed-comment-{id}"])
    if f"successed-reaction-{id}" in st.session_state:
        print(f"successed-reaction-{id}", st.session_state[f"successed-reaction-{id}"])

    if f"successed-comment-{id}" in st.session_state and st.session_state[f"successed-comment-{id}"]:
        print("successed-comment")
        st.success("コメントを送信しました")
        st.session_state[f"successed-comment-{id}"] = False

    if f"successed-reaction-{id}" in st.session_state and st.session_state[f"successed-reaction-{id}"]:
        print("successed-reaction")
        st.success(st.session_state[f"successed-reaction-{id}"])
        st.session_state[f"successed-reaction-{id}"] = False

    if any([agreed, disagreed]):
        with st.form(
            f"agree-input-{id}" if agreed else f"disagree-input-{id}",
            border=True,
        ):
            st.text_area(
                "",
                placeholder="コメントを入力...",
                key=f"text-{id}",
                height=68,
            )
            st.form_submit_button(
                "賛同する" if agreed else "反論する",
                on_click=lambda: on_submitted(id, is_agree=agreed),
            )


    return favorited, baded


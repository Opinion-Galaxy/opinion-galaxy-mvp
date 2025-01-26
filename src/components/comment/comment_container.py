from time import sleep
import streamlit as st
import logging

from .comment_expander import comment_expander

logger = logging.getLogger(__name__)

@st.fragment
def comment_container(usecase_comment, usecase_user, topics_idx):
    with st.container(border=True, key="comment-container"):
        with st.form("comment-input", border=True):
            comment_val = st.text_area("", placeholder="コメントを入力...", height=68)
            submitted = st.form_submit_button(
                "コメント",
                on_click=lambda: usecase_comment.get_comments_at_topic.clear(),
            )
            if submitted:
                try:
                    usecase_comment.post_comment(
                        st.session_state.basic_info["user_id"],
                        topics_idx + 1,
                        comment_val,
                    )
                    # usecase_comment.get_comments_at_topic.clear()
                    st.success("コメントを送信しました")
                    sleep(1)
                    st.rerun(scope="fragment")
                except Exception as e:
                    st.error("コメントが送信できませんでした")
                    logger.error(e)
        comment_expander(usecase_user, usecase_comment, topics_idx)

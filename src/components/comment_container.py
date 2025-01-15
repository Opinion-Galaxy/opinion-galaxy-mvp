import streamlit as st
from .comment_wrapper import comment_wrapper


def comment_container(usecase_comment, usecase_user, topics_idx):
    st.header("コメント")
    with st.container(border=True, key="comment-container"):
        comments_at_topic = usecase_comment.get_comments_at_topic(topics_idx + 1)
        comments_at_topic_only_parent = comments_at_topic[
            comments_at_topic["parent_id"].isnull()
        ]
        with st.form("comment-input", border=True):
            comment_val = st.text_area("", placeholder="コメントを入力...", height=68)
            submitted = st.form_submit_button("コメント")
            if submitted:
                try:
                    usecase_comment.post_comment(
                        st.session_state.basic_info["user_id"],
                        topics_idx + 1,
                        comment_val,
                    )
                    st.success("コメントを送信しました")
                except Exception as e:
                    st.error("コメントが送信できませんでした")
                    print(e)

        with st.expander("コメント一覧"):
            for i, comment in comments_at_topic_only_parent.iterrows():
                children_comments = comments_at_topic[
                    comments_at_topic["parent_id"] == comment["id"]
                ]
                comment_wrapper(
                    comment,
                    usecase_user,
                    usecase_comment,
                    topics_idx,
                    children_comments,
                )

import streamlit as st
from time import sleep
import logging

logger = logging.getLogger(__name__)


def on_submitted():
    st.session_state.submitted = True


def reset_submitted():
    st.session_state.submitted = False


def reaction_columns(id, favorite_count, bad_count, usecase_comment, topics_idx):
    reaction_cols = st.columns(4, vertical_alignment="center")
    with reaction_cols[0]:
        agreed = st.button(
            "賛同", key=f"agree_{id}", icon="👍", on_click=reset_submitted
        )
    with reaction_cols[1]:
        disagreed = st.button(
            "反論", key=f"disagree_{id}", icon="👎", on_click=reset_submitted
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
            key=f"close_{id}",
            icon=":material/close:",
            on_click=lambda: usecase_comment.get_comments_at_topic.clear(),
        )

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
                on_click=on_submitted,
            )

    if "submitted" in st.session_state and st.session_state.submitted:
        with st.spinner("コメントを送信中..."):
            try:
                usecase_comment.post_comment(
                    st.session_state.basic_info["user_id"],
                    topics_idx + 1,
                    getattr(st.session_state, f"text-{id}"),
                    parent_id=id,
                    is_agree=True,
                )
                usecase_comment.get_comments_at_topic.clear()
                st.success("コメントを送信しました")
                sleep(1)
                st.session_state.comment_fragment_rerun = True
                st.rerun(scope="fragment")
            except Exception as e:
                st.error("コメントが送信できませんでした")
                logger.error(e)
            finally:
                reset_submitted()

    if any([favorited, baded]):
        try:
            usecase_comment.reaction_at_comment(id, favorited, baded)
            usecase_comment.get_comments_at_topic.clear()
            st.success("❤️" if favorited else "×")
            sleep(1)
            st.session_state.comment_fragment_rerun = True
            st.rerun(scope="fragment")
        except Exception as e:
            st.error("リアクションが送信できませんでした")
            logger.error(e)

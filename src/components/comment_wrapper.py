import pandas as pd
from datetime import datetime
import numpy as np
import streamlit as st
import requests
from io import BytesIO
from logging import getLogger

from src.untils import format_datetime_diff

logger = getLogger(__name__)

avatar_size = 42
comment_container_style = """
<style>
    /* rem設定 */
    html {
        font-size: 15px;
    }
    /* divider余白設定 */
    html body .stMarkdown > div > hr {
        margin: 0;
    }
    /* 画像のフルスクリーンボタンの非表示 */
    div[data-testid='stFullScreenFrame'] .stElementToolbar {
        display: none;
    }
    .stVerticalBlock:has(hr) {
        gap: 0.5rem;
    }
    /* ボタンの縮小 */
    div.stButton > button {
        min-height: 2rem;
    }
    div.stButton > button > div {
        font-size: 0.75rem;
    }
    div.stButton > button > span {
        margin-right: 0.5rem;
        font-size: 0.75rem;
        width: 0.75rem;
        height: 0.75rem;
    }
    /* コメントのスタイル */
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:first-child > div.stColumn {
        min-width: unset;
    }
    /* コメントのユーザー画像 */
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:first-child > div.stColumn:first-child {
        width: 42px;
        flex-basis: 42px;
    }
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:first-child  img {
        width: 42px;
        height: 42px;
        border-radius: 42px;
    }
    /* コメントの名前・時間 */
    div[class*='st-key-comment-content-'] > div.stHorizontalBlock > div.stColumn {
        min-width: 40px;
        flex-grow: 0;
        font-size: 0.8rem;
    }
    div[class*='st-key-comment-content-'] > div.stHorizontalBlock > div.stColumn  p {
        font-size: 0.75rem;
    }
    div[class*='st-key-comment-content-'] > div.stHorizontalBlock > div.stColumn:nth-child(2) {
        color: gray;
        flex-basis: 80px;
    }
    /* コメントの内容 */
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:first-child > div.stColumn:nth-child(2) {
        flex-basis: calc(100% - 64px);
    }
    div[class*='st-key-comment-content-'] div.stMarkdown> div > p {
        line-height: 1.2;
        font-size: 0.9rem;
    }
    /* コメントのリアクション */
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:nth-child(3) {
        gap: 0.5rem;
    }
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:nth-child(3)  > div.stColumn {
        flex-basis: auto;
        min-width: unset;
        width: calc(25% - 1rem)
    }
    /* ボタン中の間隔 */
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:nth-child(3)  > div.stColumn  div.stButton > button { 
        padding: 2px 6px;
        display: flex;
        margin: 0 auto;
    }
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock:nth-child(3)  > div.stColumn  div:has(.stImage) { 
        margin: 0 auto;
    }
    div[class*='st-key-comment-content-'] {
        gap: 8px;
    }
</style>
"""


@st.cache_data
def get_random_image_bytes(comment, id):
    response = requests.get("https://picsum.photos/800")
    return BytesIO(response.content)


def on_submitted():
    st.session_state.submitted = True


def reset_submitted():
    st.session_state.submitted = False
    st.session_state.comment_val = ""


def comment_wrapper(
    comment,
    usecase_user,
    usecase_comment,
    topics_idx=0,
    children_comments=pd.DataFrame(),
):
    id = comment["id"]
    content = comment["content"]
    user = usecase_user.get_user(comment["user_id"])
    name = user["name"]
    dt = comment["commented_at"]
    is_agree = comment["is_agree"]
    favorite_count = comment["favorite_count"]
    bad_count = comment["bad_count"]
    with st.container(key=f"comment-wrapper-{id}", border=True):
        wrapper_cols = st.columns(2, vertical_alignment="center")
        with wrapper_cols[0]:
            st.image(
                get_random_image_bytes(content, id),
                width=avatar_size,
            )
        with wrapper_cols[1]:
            with st.container(key=f"comment-content-{id}"):
                name_time_cols = st.columns(3)
                with name_time_cols[0]:
                    st.write(name)
                with name_time_cols[1]:
                    st.write(
                        format_datetime_diff(
                            datetime.now() - datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                        )
                    )
                if not np.isnan(is_agree):
                    with name_time_cols[2]:
                        st.write("賛成" if is_agree else "反対")
                st.write(content)
        st.divider()
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
                str(favorite_count), key=f"favorite_{id}", icon=":material/favorite:"
            )
        with reaction_cols[3]:
            baded = st.button(
                str(bad_count), key=f"close_{id}", icon=":material/close:"
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
                    "賛同する" if agreed else "反論する", on_click=on_submitted
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
                    st.success("コメントを送信しました")
                except Exception as e:
                    st.error("コメントが送信できませんでした")
                    logger.error(e)
            reset_submitted()

        if any([favorited, baded]):
            try:
                usecase_comment.reaction_at_comment(id, favorited, baded)
            except Exception as e:
                st.error("リアクションが送信できませんでした")
                logger.error(e)
            st.success("❤️" if favorited else "×")

        if not children_comments.empty:
            for i, child_comment in children_comments.iterrows():
                comment_wrapper(
                    child_comment, usecase_user, usecase_comment, topics_idx
                )

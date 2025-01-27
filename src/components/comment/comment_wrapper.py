from dataclasses import asdict
from time import sleep
import pandas as pd
from datetime import datetime
import numpy as np
import streamlit as st
import requests
from io import BytesIO
from logging import getLogger
import aiohttp
import asyncio
from io import BytesIO
from PIL import Image
import PIL

from .reaction_columns import reaction_columns, reset_submitted
from src.untils import format_datetime_diff

logger = getLogger(__name__)

avatar_size = 42
comment_wrapper_style = """
<style>
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
        width: 100%;
    }
    div[class*='st-key-comment-wrapper-'] > div.stHorizontalBlock > div.stColumn div {
        width: 100%;
    }
    div[class*='st-key-comment-content-'] .stColumn div {
        justify-items: left;
    }
</style>
"""

async def get_random_image_bytes(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://picsum.photos/id/{id + 1}/50/50.jpg?hmac=k2yTrnX-Saxlt8-IxfGhOiSb-g3Cuqt-Vgg48L0uENs") as response:
            image_bytes = await response.read()
            if image_bytes == b'Image does not exist\n':
                image_bytes = await get_random_image_bytes(id + 1)
            return image_bytes

@st.cache_data
def get_random_image_id(id):
    return np.random.randint(1, 1000)

@st.fragment
def comment_wrapper(
    comment_id,
    usecase_user,
    usecase_comment,
    topics_idx=0,
):
    comment = asdict(usecase_comment.get_comment(comment_id))
    id = comment["id"]
    content = comment["content"]
    user = usecase_user.get_user(comment["user_id"])
    name = user.name
    dt = comment["commented_at"]
    is_agree = comment["is_agree"]
    favorite_count = comment["favorite_count"]
    bad_count = comment["bad_count"]
    images = st.session_state["user_image_dict"][topics_idx]
    children_comments = usecase_comment.get_children_comments(id)

    with st.container(key=f"comment-wrapper-{id}", border=True):
        wrapper_cols = st.columns(2, vertical_alignment="center")
        with wrapper_cols[0]:
            if comment["user_id"] not in images:
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                try:
                    task = loop.create_task(get_random_image_bytes(get_random_image_id(comment["user_id"])))
                    image_bytes = loop.run_until_complete(task)
                    images[comment["user_id"]] = image_bytes
                except Exception as e:
                    logger.error(f"画像の取得に失敗しました: {e}")
                    image_bytes = None
            else:
                image_bytes = images[comment["user_id"]]
            if image_bytes:
                try:
                    # PIL で画像を検証
                    Image.open(BytesIO(image_bytes)).verify()
                    st.image(image_bytes)
                except PIL.UnidentifiedImageError:
                    logger.error(f"取得したデータは有効な画像ではありません。 {image_bytes}")
                except Exception as e:
                    logger.error(f"画像の処理中にエラーが発生しました: {e}")
            else:
                # logger.error(image_bytes, "画像データが取得できませんでした。")
                pass
        with wrapper_cols[1]:
            with st.container(key=f"comment-content-{id}"):
                name_time_cols = st.columns(3 if is_agree is not None and not np.isnan(is_agree) else 2)
                with name_time_cols[0]:
                    st.write(name)
                with name_time_cols[1]:
                    st.write(
                        format_datetime_diff(
                            datetime.now()
                            - datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                        )
                    )
                if is_agree is not None and not np.isnan(is_agree):
                    with name_time_cols[2]:
                        st.write("賛成" if is_agree else "反対")
                st.write(content)
        st.divider()

        reaction_columns(id, favorite_count, bad_count, usecase_comment, topics_idx)

        if children_comments is not None:
            for _, child_comment in children_comments.iterrows():
                comment_wrapper(
                    child_comment["id"], usecase_user, usecase_comment, topics_idx
                )

    if f"submitted-{id}" in st.session_state and st.session_state[f"submitted-{id}"]:
        with st.spinner("コメントを送信中..."):
            try:
                usecase_comment.post_comment(
                    st.session_state.basic_info["user_id"],
                    topics_idx + 1,
                    getattr(st.session_state, f"text-{id}"),
                    parent_id=id,
                    is_agree=getattr(st.session_state, f"agreed-{id}"),
                )
                st.session_state[f"successed-comment-{id}"] = True
                usecase_comment.get_comments_at_topic.clear()
                usecase_comment.get_children_comments.clear()
                reset_submitted(id)
                st.rerun(scope="fragment")
            except Exception as e:
                st.error("コメントが送信できませんでした")
                logger.error(e)
                reset_submitted(id)

    favorited = st.session_state[f"favorite_{id}"]
    baded = st.session_state[f"bad_{id}"]
    if any([favorited, baded]):
        try:
            usecase_comment.reaction_at_comment(id, favorited, baded)
            st.session_state[f"successed-reaction-{id}"] = "❤️" if favorited else "×"
            st.session_state.comment_fragment_rerun = True
            usecase_comment.get_comments_at_topic.clear()
            usecase_comment.get_children_comments.clear()
            st.rerun(scope="fragment")
        except Exception as e:
            st.error("リアクションが送信できませんでした")
            logger.error(e)
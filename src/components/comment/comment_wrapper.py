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

from .reaction_columns import reaction_columns
from src.untils import format_datetime_diff

logger = getLogger(__name__)

avatar_size = 42
comment_wrapper_style = """
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

async def get_random_image_bytes(comment, id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://picsum.photos/id/{id + 1}/800/800.jpg?hmac=k2yTrnX-Saxlt8-IxfGhOiSb-g3Cuqt-Vgg48L0uENs") as response:
            image_bytes = await response.read()
            return image_bytes

@st.cache_data
def get_random_image_id(id):
    return np.random.randint(1, 1000)

async def comment_wrapper(
    comment,
    usecase_user,
    usecase_comment,
    topics_idx=0,
    children_comments=pd.DataFrame(),
):
    id = comment["id"]
    content = comment["content"]
    user = usecase_user.get_user(comment["user_id"])
    name = user.name
    dt = comment["commented_at"]
    is_agree = comment["is_agree"]
    favorite_count = comment["favorite_count"]
    bad_count = comment["bad_count"]

    image_id = get_random_image_id(id)

    with st.container(key=f"comment-wrapper-{id}", border=True):
        wrapper_cols = st.columns(2, vertical_alignment="center")
        with wrapper_cols[0]:
            image_bytes = await get_random_image_bytes(content, image_id)
            if image_bytes:
                try:
                    # PIL で画像を検証
                    Image.open(BytesIO(image_bytes)).verify()
                    st.image(image_bytes)
                except PIL.UnidentifiedImageError:
                    logger.error("取得したデータは有効な画像ではありません。")
                except Exception as e:
                    logger.error(f"画像の処理中にエラーが発生しました: {e}")
            else:
                logger.error("画像データが取得できませんでした。")
        with wrapper_cols[1]:
            with st.container(key=f"comment-content-{id}"):
                name_time_cols = st.columns(3)
                with name_time_cols[0]:
                    st.write(name)
                with name_time_cols[1]:
                    st.write(
                        format_datetime_diff(
                            datetime.now()
                            - datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
                        )
                    )
                if is_agree is not None and not np.isnan(is_agree):
                    with name_time_cols[2]:
                        st.write("賛成" if is_agree else "反対")
                st.write(content)
        st.divider()
        reaction_columns(id, favorite_count, bad_count, usecase_comment, topics_idx)

        if not children_comments.empty:
            tasks = [
                comment_wrapper(
                    child_comment, usecase_user, usecase_comment, topics_idx
                )
                for _, child_comment in children_comments.iterrows()
            ]
            await asyncio.gather(*tasks)

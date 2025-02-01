import asyncio
from io import BytesIO
from time import sleep
import streamlit as st
from .comment_wrapper import comment_wrapper, get_random_image_bytes, get_random_image_id
import plotly.express as px
from PIL import Image

async def run_tasks(tasks):
    try:
        result = await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.CancelledError:
        st.error("タスクがキャンセルされました。")
    except Exception as e:
        st.error("コメントの取得に失敗しました")
        st.error(e)
    return result

def cancel_existing_tasks():
    if 'tasks' not in st.session_state or not st.session_state.tasks:
        return
    # if 'event_loop' not in st.session_state:
    #     return
    for task in st.session_state.tasks:
        if not task.done():
            task.cancel()
    # タスクがキャンセル処理中なので、イベントループ上で実際に待つ
    loop = st.session_state.event_loop
    if loop.is_running():
        # loop が既に動いている場合は、shutdown_asyncgens() 等で後始末
        # run_until_complete() は使えないので、適宜再帰的にキャンセル待ちしてもよい
        if any(not task.done() for task in st.session_state.tasks):
            sleep(0.5)
            cancel_existing_tasks()
        else:
            loop.stop()
            # if not loop.is_running():
            #     loop.close()
    else:
        # イベントループが走っていなければ、キャンセル完了を待つ
        try:
            loop.run_until_complete(asyncio.gather(*st.session_state.tasks, return_exceptions=True))
        except RuntimeError:
            # イベントループが閉じていたら無視でもOK
            pass
    if loop.is_running():
        loop.stop()
    # else:
    #     loop.close()
    # del st.session_state.event_loop
    st.session_state.tasks = []



def comment_expander(
    usecase_user,
    usecase_comment,
    topics_idx,
):
    cancel_existing_tasks()
    comments_at_topic = usecase_comment.get_comments_at_topic(topics_idx + 1)
    comments_at_topic_only_parent = comments_at_topic[
        comments_at_topic["parent_id"].isnull()
        | (comments_at_topic["parent_id"] == "None")
    ]
    unique_user_id = comments_at_topic["user_id"].unique()

    if 'event_loop' not in st.session_state:
        try:
            st.session_state.event_loop = asyncio.get_event_loop()
        except RuntimeError:
            st.session_state.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(st.session_state.event_loop)
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    loop = st.session_state.event_loop
    st.session_state.tasks = [loop.create_task(get_random_image_bytes(get_random_image_id(user_id)))  for user_id in unique_user_id]
    results = loop.run_until_complete(run_tasks(st.session_state.tasks))

    user_image_dict = dict(zip(unique_user_id, results))
    if "user_image_dict" not in st.session_state:
        st.session_state["user_image_dict"] = {}
    st.session_state["user_image_dict"][topics_idx] = user_image_dict
    if all(task.done() for task in st.session_state.tasks):
        loop.close()
        del st.session_state.event_loop
        del st.session_state.tasks

    with st.expander(
        "コメント一覧",
        expanded="comment_fragment_rerun" in st.session_state
        and st.session_state.comment_fragment_rerun,
    ):
        for i, comment in comments_at_topic_only_parent.iterrows():
            # children_comments = comments_at_topic[
            #     comments_at_topic["parent_id"] == comment["id"]
            # ]
            comment_wrapper(
                comment.id,
                usecase_user,
                usecase_comment,
                topics_idx,
                # children_comments,
            )

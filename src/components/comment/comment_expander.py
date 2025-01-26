import asyncio
from time import sleep
import streamlit as st
from .comment_wrapper import comment_wrapper

async def run_tasks(tasks):
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.CancelledError:
        st.error("タスクがキャンセルされました。")
    except Exception as e:
        st.error("コメントの取得に失敗しました")
        st.error(e)
    return

def cancel_existing_tasks():
    if 'tasks' not in st.session_state or not st.session_state.tasks:
        return
    if 'event_loop' not in st.session_state:
        return
    for task in st.session_state.tasks:
        if not task.done():
            task.cancel()
    # タスクがキャンセル処理中なので、イベントループ上で実際に待つ
    loop = st.session_state.event_loop
    if loop.is_running():
        # loop が既に動いている場合は、shutdown_asyncgens() 等で後始末
        # run_until_complete() は使えないので、適宜再帰的にキャンセル待ちしてもよい
        if not any(task.done() for task in st.session_state.tasks):
            cancel_existing_tasks()
        else:
            loop.stop()
            if not loop.is_running():
                loop.close()
    else:
        # イベントループが走っていなければ、キャンセル完了を待つ
        try:
            loop.run_until_complete(asyncio.gather(*st.session_state.tasks, return_exceptions=True))
        except RuntimeError:
            # イベントループが閉じていたら無視でもOK
            pass
    if loop.is_running():
        loop.stop()
    else:
        loop.close()
    del st.session_state.event_loop
    st.session_state.tasks = []

@st.fragment
def comment_expander(
    usecase_user,
    usecase_comment,
    topics_idx,
):
    
    comments_at_topic = usecase_comment.get_comments_at_topic(topics_idx + 1)
    comments_at_topic_only_parent = comments_at_topic[
        comments_at_topic["parent_id"].isnull()
        | (comments_at_topic["parent_id"] == "None")
    ]
    with st.expander(
        "コメント一覧",
        expanded="comment_fragment_rerun" in st.session_state
        and st.session_state.comment_fragment_rerun,
    ):
        cancel_existing_tasks()
        if 'event_loop' not in st.session_state:
            st.session_state.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(st.session_state.event_loop)
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        loop = st.session_state.event_loop
        tasks = []
        for i, comment in comments_at_topic_only_parent.iterrows():
            children_comments = comments_at_topic[
                comments_at_topic["parent_id"] == comment["id"]
            ]
            tasks.append(loop.create_task(comment_wrapper(
                        comment,
                        usecase_user,
                        usecase_comment,
                        topics_idx,
                        children_comments,
            )))
        st.session_state.tasks = tasks
        # if not loop.is_running():
        loop.run_until_complete(run_tasks(tasks))
        if all(task.done() for task in st.session_state.tasks):
            loop.stop()
            loop.close()
            del st.session_state.event_loop
            del st.session_state.tasks
        # loop.close()
        # del st.session_state.event_loop
        # del st.session_state.tasks
        # loop.close()
        # del st.session_state.event_loop
        # st.session_state.tasks = []
        # if st.session_state.tasks:
        #     with st.spinner("コメントを読み込んでいます..."):
        #         while not all(task.done() for task in st.session_state.tasks):
        #             loop.run_until_complete(asyncio.sleep(0.1))
        #     st.session_state.tasks = []

        # for i, comment in comments_at_topic_only_parent.iterrows():
        #     children_comments = comments_at_topic[
        #         comments_at_topic["parent_id"] == comment["id"]
        #     ]
        #     comment_wrapper(
        #         comment,
        #         usecase_user,
        #         usecase_comment,
        #         topics_idx,
        #         children_comments,
        #     )

import asyncio
import streamlit as st
from .comment_wrapper import comment_wrapper


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
        tasks = []
        for i, comment in comments_at_topic_only_parent.iterrows():
            children_comments = comments_at_topic[
                comments_at_topic["parent_id"] == comment["id"]
            ]
            tasks.append(
                comment_wrapper(
                    comment,
                    usecase_user,
                    usecase_comment,
                    topics_idx,
                    children_comments,
                )
            )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
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

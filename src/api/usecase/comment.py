from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import streamlit as st
import uuid

import pandas as pd


@dataclass
class CommentEntity:
    user_id: str
    topic_id: int
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    commented_at: datetime = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    parent_id: Optional[str] = None
    favorite_count: int = 0
    bad_count: int = 0
    is_agree: int = 0


class Comment:
    def __init__(self, driver_comment):
        self.repository = driver_comment

    def get_all_comments(self):
        comment_rows = self.repository.get_all()
        comment_df = pd.DataFrame(comment_rows, columns=comment_rows[0].keys())
        return comment_df

    def get_comment(self, comment_id: uuid.UUID) -> CommentEntity:
        comment_row = self.repository.get(comment_id)
        return CommentEntity(**comment_row)

    @st.cache_data
    def get_comments_at_topic(_self, topic_id: int):
        comment_rows = _self.repository.find_all(topic_id=topic_id)
        comment_df = pd.DataFrame(comment_rows, columns=comment_rows[0].keys())
        return comment_df

    def get_children_comments(self, parent_id):
        comment_rows = self.repository.find_all(parent_id=parent_id)
        comment_df = pd.DataFrame(comment_rows, columns=comment_rows[0].keys())
        return comment_df

    def post_comment(self, user_id, topic_id, comment, parent_id=None, is_agree=None):
        comment = CommentEntity(
            user_id=user_id,
            topic_id=topic_id,
            content=comment,
            parent_id=parent_id,
            is_agree=is_agree,
        )
        return self.repository.post(comment=comment)

    def reaction_at_comment(self, comment_id, favorited, baded):
        try:
            comment = dict(self.repository.get(comment_id))
        except Exception:
            return None

        if favorited:
            comment["favorite_count"] += 1
        if baded:
            comment["bad_count"] += 1

        return self.repository.put(
            comment_id,
            CommentEntity(**comment),
        )

from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class CommentEntity:
    id: uuid.UUID
    commented_at: datetime
    user_id: uuid.UUID
    topic_id: int
    content: str
    parent_id: uuid.UUID
    favorite_count: int
    bad_count: int
    is_agree: int

    def __init__(
        self,
        user_id: uuid.UUID,
        topic_id: int,
        comment: str,
        parent_id: uuid.UUID = None,
        is_agree: int = None,
    ):
        self.id = uuid.uuid4()
        self.commented_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.user_id = user_id
        self.topic_id = topic_id
        self.content = comment
        self.parent_id = parent_id
        self.favorite_count = 0
        self.bad_count = 0
        self.is_agree = is_agree if is_agree is None else int(is_agree)


class Comment:
    def __init__(self, driver):
        self.repository = driver.Comment()

    def get_comment(self, comment_id):
        return self.repository.get(comment_id)

    def get_comments_at_topic(self, topic_id):
        return self.repository.find_all(topic_id=topic_id)

    def get_children_comments(self, parent_id):
        return self.repository.find_all(parent_id=parent_id)

    def post_comment(self, user_id, topic_id, comment, parent_id=None, is_agree=None):
        comment = CommentEntity(
            user_id=user_id,
            topic_id=topic_id,
            comment=comment,
            parent_id=parent_id,
            is_agree=is_agree,
        )
        return self.repository.post(comment=comment)

    def reaction_at_comment(self, comment_id, favorited, baded):
        try:
            comment = self.repository.get(comment_id)
        except Exception:
            return None

        if favorited:
            comment["favorite_count"] += 1
        if baded:
            comment["bad_count"] += 1

        return self.repository.put(comment_id, comment)

from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class AnswerEntity:
    id: int
    user_id: uuid.UUID
    answered_at: datetime
    topic_id: int
    value: str

    def __init__(self, user_id, topic_id, value):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.answered_at = datetime.now()
        self.topic_id = topic_id
        self.value = value


class Answer:
    def __init__(self, driver):
        self.answer_repo = driver.Answer()
        self.topic_repo = driver.Topic()

    def get_all_answers(self):
        all_df = self.answer_repo.get_all()
        topic_df = self.topic_repo.get_all()
        all_df["topic_id"] = all_df["topic_id"].map(
            topic_df.set_index("id")["topic"].to_dict()
        )
        return all_df

    def get_user_answers(self, user_id):
        all_df = self.answer_repo.get_all()
        topic_df = self.topic_repo.get_all()
        all_df["topic_id"] = all_df["topic_id"].map(
            topic_df.set_index("id")["topic"].to_dict()
        )
        return all_df[all_df["user_id"] == user_id]

    def update_answer(self, id, value):
        return self.answer_repo.put(id, value)

    def create_answer(self, user_id, topic_id, value):
        answer = AnswerEntity(user_id=user_id, topic_id=topic_id, value=value)
        return self.answer_repo.post(answer)

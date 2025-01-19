from dataclasses import dataclass, field
from datetime import datetime
import uuid

import pandas as pd


@dataclass
class AnswerEntity:
    user_id: str
    topic_id: int
    value: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    answered_at: datetime = field(default_factory=datetime.now)


class Answer:
    def __init__(self, answer_driver):
        self.answer_repo = answer_driver

    def get_all_answers(self):
        all_rows = self.answer_repo.get_all()
        all_df = pd.DataFrame(all_rows, columns=all_rows[0].keys())
        return all_df

    def get_user_answers(self, user_id: uuid.UUID):
        user_answer_rows = self.answer_repo.find_by_id(user_id=str(user_id))
        if not user_answer_rows:
            return pd.DataFrame()
        return pd.DataFrame(user_answer_rows, columns=user_answer_rows[0].keys())

    def update_answer(self, id, value):
        return self.answer_repo.put(id, value)

    def create_answer(self, user_id, topic_id, value):
        answer = AnswerEntity(user_id=user_id, topic_id=topic_id, value=value)
        return self.answer_repo.post(answer)

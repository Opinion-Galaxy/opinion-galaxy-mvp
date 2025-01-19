from datetime import datetime
from src.api.usecase.answer import AnswerEntity


class Answer:
    def __init__(self, conn):
        self.conn = conn

    def find_by_id(self, user_id=None, topic_id=None):
        if user_id is None:
            cursor = self.conn.execute(
                "SELECT * FROM answers WHERE topic_id = ?", (topic_id,)
            )
        elif topic_id is None:
            cursor = self.conn.execute(
                "SELECT * FROM answers WHERE user_id = ?", (user_id,)
            )
        else:
            cursor = self.conn.execute(
                "SELECT * FROM answers WHERE user_id = ? AND topic_id = ?",
                (user_id, topic_id),
            )
        result = cursor.fetchall()
        return result if result else []

    def get_all(self):
        cursor = self.conn.execute(
            "SELECT * FROM answers JOIN topics ON answers.topic_id = topics.id"
        )  # merge with topics
        return cursor.fetchall()

    def get(self, id):
        cursor = self.conn.execute("SELECT * FROM answers WHERE id = ?", (id,))
        return cursor.fetchone()

    def post(self, answer: AnswerEntity):
        query = """
        INSERT INTO answers (id, value, user_id, topic_id)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (answer.id, answer.value, answer.user_id, answer.topic_id),
        )
        self.conn.commit()
        return answer.id

    def put(self, id, answer_value):
        query = """
        UPDATE answers
        SET value = ?, answered_at = ?
        WHERE id = ?
        """
        self.conn.execute(query, (answer_value, datetime.now(), id))
        self.conn.commit()

    def close(self):
        self.conn.close()

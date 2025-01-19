import sqlite3
import pandas as pd

from src.api.driver.utils import generate_uuid


# class Topic:
#     def __init__(self):
#         self.df = pd.read_csv("data/topics.csv")

#     def get(self, topic_id):
#         return self.df.iloc[topic_id].copy()

#     def get_all(self):
#         return self.df.copy()


class Topic:
    def __init__(self, conn):
        self.conn = conn
        # self.create_table()

    # def create_table(self):
    #     query = """
    #     CREATE TABLE IF NOT EXISTS topics (
    #         id TEXT PRIMARY KEY,
    #         topic TEXT NOT NULL
    #     );
    #     """
    #     self.conn.execute(query)
    #     self.conn.commit()

    def get(self, topic_id):
        cursor = self.conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        return cursor.fetchone()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM topics")
        return cursor.fetchall()

    # def post(self, topic):
    #     query = "INSERT INTO topics (id, topic) VALUES (?, ?)"
    #     new_id = generate_uuid()
    #     self.conn.execute(query, (new_id, topic.topic))
    #     self.conn.commit()
    #     return new_id

    def close(self):
        self.conn.close()

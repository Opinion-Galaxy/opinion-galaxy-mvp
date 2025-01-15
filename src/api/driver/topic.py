import pandas as pd


class Topic:
    def __init__(self):
        self.df = pd.read_csv("data/topics.csv")

    def get(self, topic_id):
        return self.df.iloc[topic_id].copy()

    def get_all(self):
        return self.df.copy()

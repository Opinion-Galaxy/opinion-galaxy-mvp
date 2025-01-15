import pandas as pd


class Comment:
    def __init__(self):
        self.df = pd.read_csv("data/comments.csv")

    def get(self, comment_id):
        return self.df.iloc[comment_id].copy()

    def find_all(self, topic_id=None, parent_id=None):
        df = self.df.copy()
        if topic_id:
            df = df[df["topic_id"] == topic_id]
        if parent_id:
            df = df[df["parent_id"] == parent_id]
        return df

    def post(self, comment):
        comment_df = pd.DataFrame(comment.__dict__, index=[0])
        self.df = pd.concat([self.df, comment_df], axis=0)
        self.df.to_csv("data/comments.csv", index=False)

    def put(self, comment_id, comment):
        self.df.iloc[comment_id] = comment
        self.df.to_csv("data/comments.csv", index=False)

import pandas as pd


class User:
    def __init__(self):
        self.df = pd.read_csv("data/users.csv", parse_dates=["created_at"])

    def get(self, user_id):
        return self.df[self.df["id"] == user_id]

    def get_all(self):
        return self.df.copy()

    def post(self, user):
        user_df = pd.DataFrame(user.__dict__, index=[0])
        self.df = pd.concat([self.df, user_df], ignore_index=True)
        self.df.to_csv("data/users.csv", index=False)

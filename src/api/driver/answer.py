import pandas as pd


class Answer:
    def __init__(self):
        self.df = pd.read_csv(
            "data/answers.csv", dtype={"value": "Int64"}, parse_dates=["answered_at"]
        )

    def get_id(self, user_id, topic_id):
        return (
            self.df.loc[
                (self.df["user_id"] == user_id) & (self.df["topic_id"] == topic_id),
                "id",
            ]
            .copy()
            .values[0]
        )

    def get_all(self):
        return self.df.copy()

    def get(self, id):
        return self.df.loc[self.df["id"] == id].copy()

    def post(self, answer):
        answer_df = pd.DataFrame(answer.__dict__, index=[0])
        self.df = pd.concat([self.df, answer_df], ignore_index=True)
        self.df.to_csv("data/answers.csv", index=False)
        return

    def put(self, id, answer_value):
        self.df.loc[self.df["id"] == id, "value"] = answer_value
        self.df.to_csv("data/answers.csv", index=False)
        return

import os
import sqlite3
import pandas as pd

DATA_DIR = "/app/data"

conn = sqlite3.connect(os.path.join(DATA_DIR, "database", "database.db"))

answer_data = pd.read_sql("SELECT * FROM answers", conn)
user_data = pd.read_sql("SELECT * FROM users", conn)

answer_city = answer_data.merge(
    user_data[["id", "prefecture", "city"]], left_on="user_id", right_on="id"
)
answer_city = answer_city[answer_city["prefecture"] == "東京都"].drop(
    "prefecture", axis=1
)
answer_city["value"] = answer_city["value"].replace({1: "賛成", 0: "中立", -1: "反対"})
answer_by_city = (
    answer_city.groupby(["city", "topic_id", "value"]).size().unstack().fillna(0)
)
answer_by_city = answer_by_city.reset_index()
answer_by_city = answer_by_city.merge(
    pd.read_csv(os.path.join(DATA_DIR, "topics.csv")),
    left_on="topic_id",
    right_on="id",
    how="left",
)
answer_by_city = answer_by_city.drop(["id", "topic_id"], axis=1)
# answer_by_city = answer_by_city
# answer_by_city.to_csv(os.path.join(DATA_DIR, "answer_by_city.csv"), encoding="utf-8")

answer_by_city.merge(
    pd.read_csv(os.path.join(DATA_DIR, "tokyo_election_area.csv")),
    left_on="city",
    right_on="市区町村",
    how="left",
).drop("市区町村", axis=1).set_index(["city", "topic"]).to_csv(
    os.path.join("/var/lib/litefs/data_for_train", "answer_by_tokyo_election_area.csv"),
    encoding="utf-8",
)

import pickle
import numpy as np
import re
import itertools
import pandas as pd
import streamlit as st


@st.cache_data
def get_candidate_embs():
    with open("data/predict/candidate_embeddings.pkl", "rb") as f:
        candidate_embs = pickle.load(f)
    return candidate_embs


@st.cache_data
def get_theme_embs():
    with open("data/predict/topic_embeddings.pkl", "rb") as f:
        theme_embs = pickle.load(f)
    return theme_embs


@st.cache_data
def get_answer_by_tokyo_election_area():
    return pd.read_csv("data/answer_by_tokyo_election_area.csv")


@st.cache_data
def create_dataset(dummy_election):
    candidate_enbs = get_candidate_embs()
    theme_embs = get_theme_embs()
    answer_by_tokyo_election_area = get_answer_by_tokyo_election_area()
    data_list = []

    for i, row in dummy_election.iterrows():
        target_answer = (
            answer_by_tokyo_election_area[
                answer_by_tokyo_election_area["選挙区"] == row["選挙区"]
            ]
            .pivot(
                index=["city", "選挙区"],
                columns="topic",
                values=["賛成", "反対", "中立"],
            )
            .reset_index(level=1)
            .set_index("選挙区")
        )
        for topic in theme_embs.keys():
            for i, _ in enumerate(re.split(r"・|、", row["主要政策"])):
                area = row["選挙区"]
                name = row["候補者名"]
                row[f"{topic}_{i}"] = np.corrcoef(
                    theme_embs[topic], candidate_enbs[area][name][i]
                )[0, 1]
            multiple_value = itertools.product(
                row[row.index.str.startswith(topic)].values,
                target_answer.loc[:, target_answer.columns.get_level_values(1) == topic]
                .mean()
                .values,
            )
            index = list(
                itertools.product(
                    row[row.index.str.startswith(topic)].index,
                    target_answer.loc[
                        :, target_answer.columns.get_level_values(1) == topic
                    ].columns,
                )
            )
            index_flat = [f"{a}_{b[0]}" for a, b in index]
            # リストに変換して掛け算
            product_results = pd.Series(
                [a * b for a, b in multiple_value], index=index_flat
            ).astype(float)
            row = pd.concat([row, product_results])
        target_answer.columns = ["_".join(col) for col in target_answer.columns]
        row = pd.concat([row, target_answer.mean()])
        data_list.append(row)
    dataset = pd.concat(data_list, axis=1).T
    for col in dataset.columns:
        dataset[col] = pd.to_numeric(dataset[col], errors="ignore")
    dataset = dataset.drop(["主要政策", "経歴・特徴"], axis=1)
    object_columns = dataset.select_dtypes(include="object").columns.tolist()
    object_columns.remove("選挙区")
    dataset = pd.get_dummies(dataset, columns=object_columns, drop_first=True)
    return dataset


def predict(X_test, y_test):
    with open("data/predict/best_model_for_1.pkl", "rb") as f:
        model = pickle.load(f)
    return model.predict(X_test)

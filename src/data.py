import pandas as pd
import numpy as np
import streamlit as st
from pandera.typing import DataFrame


from .type import Data, Dataset, DatasetWithLonLat, Topics, OpinionMap
from .const import get_prefecture_city, topics, opinion_map


# サンプルデータの作成
@st.cache_data
def load_data() -> DataFrame[Data]:
    data = pd.read_csv(
        "data/dummy_political_opinions_with_datetime.csv",
        parse_dates=["response_datetime"],
        dtype={topic: "Int64" for topic in topics},
        converters={
            topic: lambda x: opinion_map[str(int(float(x)))]
            if not pd.isna(x) and x != ""
            else x
            for topic in topics
        },
    ).sort_values("response_datetime")
    data["age"] = pd.cut(
        data["age"],
        np.arange(10, 100, 10),
        labels=np.arange(10, 90, 10).astype(str).astype(object) + "代",
    )
    data["response_datetime"] = data["response_datetime"].dt.strftime("%Y-%m-%d")
    return data


def create_cumsum_radio_data(
    data: Data, selected_topic: Topics, agree_neutral_disagree="賛成"
) -> pd.DataFrame:
    selected_data = data[data[selected_topic] == agree_neutral_disagree].copy()
    cumsum_data = (
        selected_data.groupby(["sex", "age", "response_datetime", "address"])[
            selected_topic
        ]
        .count()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum(axis=1)
    )
    grouped_count = (
        data.groupby(["sex", "age", "response_datetime", "address"])[selected_topic]
        .count()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum(axis=1)
    )
    cumsum_radio_data = cumsum_data.div(
        grouped_count,
        axis=0,
    )
    cumsum_radio_data["agree"] = agree_neutral_disagree
    return cumsum_radio_data


@st.cache_data
def create_dataset(
    data: Data, selected_topic: Topics, opinion_map: OpinionMap
) -> DataFrame[Dataset]:
    return (
        pd.concat(
            [
                create_cumsum_radio_data(data, selected_topic, i)
                for i in opinion_map.values()
            ]
        )
        .melt(ignore_index=False, value_name="cumsum", id_vars=["agree"])
        .reset_index()
    )


@st.cache_data
def merge_lonlat(data: pd.DataFrame) -> DataFrame[DatasetWithLonLat]:
    prefecture_city = get_prefecture_city()
    prefecture_city["address"] = (
        prefecture_city["都道府県名"] + prefecture_city["市区町村名"]
    )
    prefecture_city_lonlat = (
        prefecture_city.groupby(["address"])[["緯度", "経度"]]
        .mean()
        .reset_index()
        .rename(columns={"緯度": "lat", "経度": "lon"})
    )
    data = data.merge(
        prefecture_city_lonlat, how="left", left_on="address", right_on="address"
    )
    del prefecture_city, prefecture_city_lonlat
    return data


def check_same_data(
    data: Data,
    selected_topic: Topics,
    agree: bool,
    disagree: bool,
    age: str,
    sex: str,
    address: str,
) -> pd.DataFrame:
    same_data = data[
        (data["age"] == age) & (data["sex"] == sex) & (data["address"] == address)
    ]

    if not same_data.empty:
        print("以下のデータがすでに存在します")
        print(same_data)
        if same_data[selected_topic].iloc[0] == int(agree - disagree):
            st.write("すでに同じ意見が登録されています")
            st.stop()

    return same_data


def add_new_data(
    data: Data,
    same_data: pd.DataFrame,
    selected_topic: Topics,
    agree: bool,
    disagree: bool,
    age: str,
    sex: str,
    address: str,
) -> None:
    existed_data = (
        {topic: np.nan for topic in (set(topics) - {selected_topic})}
        if same_data.empty
        else same_data[list(set(topics) - {selected_topic})]
        .iloc[0]
        .astype("Int64")
        .to_dict()
    )
    existed_data["ID"] = (
        same_data["ID"].iloc[0] if not same_data.empty else data["ID"].max() + 1
    )
    new_data = pd.DataFrame(
        {
            "response_datetime": pd.Timestamp.now(),
            "age": age,
            "sex": sex,
            "address": address,
            selected_topic: int(agree - disagree),
            **existed_data,
        },
        index=[0],
    )
    if not same_data.empty:
        data = data.drop(same_data.index)
    data = pd.concat([data, new_data], axis=0, ignore_index=True)
    print("以下のデータを追加しました")
    print(new_data)
    data.to_csv("data/dummy_political_opinions_with_datetime.csv", index=False)

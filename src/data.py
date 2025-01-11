import pandas as pd
import numpy as np
import streamlit as st
from pandera.typing import DataFrame


from .type import Data, Dataset, DatasetWithLonLat, Topics, OpinionMap
from .const import topics, opinion_map


# サンプルデータの作成
@st.cache_data
def load_data() -> DataFrame[Data]:
    data = pd.read_csv(
        "data/dummy_political_opinions_with_datetime.csv",
        parse_dates=["response_datetime"],
        converters={topic: lambda x: opinion_map[x] for topic in topics},
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

    cumsum_radio_data = cumsum_data.div(
        data.groupby(["sex", "age", "response_datetime", "address"])[selected_topic]
        .count()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum(axis=1),
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
    prefecture_city = pd.read_csv(
        "data/prefecture_city_lonlat.csv",
        encoding="utf-8",
    )
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

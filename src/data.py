import pandas as pd
import numpy as np
import streamlit as st
from pandera.typing import DataFrame
from logging import getLogger

logger = getLogger(__name__)

from src.api import usecase

from .type import Data, DatasetWithLonLat, Topics
from .const import get_prefecture_city, topics, opinion_map


# サンプルデータの作成
@st.cache_data(
    hash_funcs={
        usecase.answer.Answer: lambda x: x.get_all_answers().shape,
        usecase.user.User: lambda x: x.get_all_users().shape,
    }
)
def load_data(usecase_answer, usecase_user) -> pd.DataFrame:
    # `opinion_map` を事前に適用するためにデータを読み込んだ後に変換
    answer_data = usecase_answer.get_all_answers()
    user_data = usecase_user.get_all_users()
    data = pd.merge(
        answer_data, user_data, left_on="user_id", right_on="id", how="left"
    )
    data["sex"] = data["is_male"].astype(bool).map({True: "男性", False: "女性"})
    data = data.drop(columns=["id_x", "is_male", "created_at"]).rename(
        columns={"answered_at": "response_datetime", "topic_id": "topic"}
    )
    data["value"] = (
        data["value"]
        .astype("Int64")
        .astype("Float64")
        .astype("Int64")
        .astype(str)
        .map(opinion_map)
    )
    # 年齢のカテゴリ分けを一度に行う
    data["age"] = pd.cut(
        data["age"],
        bins=np.arange(10, 100, 10),
        labels=[f"{i}代" for i in range(10, 90, 10)],
        right=False,
    )

    # 日付フォーマットを一度に適用
    data["response_datetime"] = data["response_datetime"].dt.strftime("%Y-%m-%d")

    return data


# -----------------------------------------------------------
# もとの create_dataset 相当の機能をまとめて実行する
# -----------------------------------------------------------
@st.cache_data
def create_dataset(data: pd.DataFrame, selected_topic: str) -> pd.DataFrame:
    """
    create_cumsum_radio_data_all で作った結果を melt して
    ['agree', 'cumsum'] 列を持たせる形にする。
    """
    # まとめて累積処理
    # groupby して各意見の件数を pivot
    logger.info(data)
    grouped = (
        data[data["topic"] == selected_topic]
        .groupby(["sex", "age", "response_datetime", "address", "value"])["value"]
        .count()
        .unstack(level=-1, fill_value=0)  # 意見ごとに列を展開
        .sort_index(axis=1)  # 賛成・中立・反対などの列順を確定
        .sort_index()  # index 軸([sex, age, response_datetime, address])の順序も確定
    )

    # 累積和の総計（行合計）を計算して、各列の値を割り算
    total_cumsum = grouped.sum(axis=1)
    cumsum_ratio = grouped.div(total_cumsum, axis=0).reset_index()

    # melt して 'agree' 列 (賛成・中立・反対...) と 'cumsum' 列を作成
    return cumsum_ratio.melt(
        id_vars=["sex", "age", "response_datetime", "address"],
        var_name="agree",
        value_name="cumsum",
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
        logger.info("以下のデータがすでに存在します")
        logger.info(same_data)
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
    logger.info("以下のデータを追加しました")
    logger.info(new_data)
    data.to_csv("data/dummy_political_opinions_with_datetime.csv", index=False)

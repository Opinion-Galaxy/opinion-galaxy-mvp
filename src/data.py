import pandas as pd
import numpy as np
import streamlit as st
from logging import getLogger
from src.api import usecase

from .const import opinion_map

logger = getLogger(__name__)


# サンプルデータの作成
@st.cache_data(
    show_spinner=False,
    hash_funcs={
        usecase.answer.Answer: lambda x: x.get_answers_length(),
        usecase.user.User: lambda x: x.get_users_length(),
    },
)
def load_data(
    usecase_answer: usecase.answer.Answer, usecase_user: usecase.answer.Answer
) -> pd.DataFrame:
    # `opinion_map` を事前に適用するためにデータを読み込んだ後に変換
    answer_data = usecase_answer.get_all_answers()
    user_data = usecase_user.get_all_users()
    data = pd.merge(
        answer_data, user_data, left_on="user_id", right_on="id", how="left"
    )
    data["sex"] = data["is_male"].astype(bool).map({True: "男性", False: "女性"})
    data = data.drop(columns=["id_x", "is_male", "created_at"]).rename(
        columns={"answered_at": "response_datetime", "id_y": "id"}
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
    data["response_datetime"] = pd.to_datetime(data["response_datetime"]).dt.strftime(
        "%Y-%m-%d"
    )
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
    logger.info("data", data)
    grouped = (
        data[data["topic"] == selected_topic]
        .groupby(["sex", "age", "response_datetime", "prefecture", "value"])["value"]
        .count()
        .unstack(level=-1, fill_value=0)  # 意見ごとに列を展開
        .sort_index(axis=1)  # 賛成・中立・反対などの列順を確定
        .sort_index()  # index 軸([sex, age, response_datetime, prefecture, city])の順序も確定
    )

    # 累積和の総計（行合計）を計算して、各列の値を割り算
    total_cumsum = grouped.sum(axis=1)
    cumsum_ratio = grouped.div(total_cumsum, axis=0).reset_index()

    # melt して 'agree' 列 (賛成・中立・反対...) と 'cumsum' 列を作成
    return cumsum_ratio.melt(
        id_vars=["sex", "age", "response_datetime", "prefecture"],
        var_name="agree",
        value_name="cumsum",
    )


# def merge_lonlat(data: pd.DataFrame) -> DataFrame[DatasetWithLonLat]:
#     prefecture_city = get_prefecture_city()
#     prefecture_city["prefecture", "city"] = (
#         prefecture_city["都道府県名"] + prefecture_city["市区町村名"]
#     )
#     prefecture_city_lonlat = (
#         prefecture_city.groupby(["prefecture", "city"])[["緯度", "経度"]]
#         .mean()
#         .reset_index()
#         .rename(columns={"緯度": "lat", "経度": "lon"})
#     )
#     data = data.merge(
#         prefecture_city_lonlat, how="left", left_on="prefecture", "city", right_on="prefecture", "city"
#     )
#     del prefecture_city, prefecture_city_lonlat
#     return data

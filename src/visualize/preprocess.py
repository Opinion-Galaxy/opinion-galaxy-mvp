from typing import Tuple
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from ..type import Data, DatasetWithLonLat, Topics, Dataset


def preprocess_basic_pie(data: DataFrame[Data], selected_topic: Topics) -> pd.DataFrame:
    return (
        data.loc[data["topic"] == selected_topic, "value"]
        .value_counts()
        .to_frame()
        .reset_index()
    )


def preprocess_time_series_area(cumsum_radio_data: DataFrame[Dataset]) -> pd.DataFrame:
    time_cumsum = (
        cumsum_radio_data.groupby(["response_datetime", "agree"])["cumsum"]
        .mean()
        .unstack(level=0, fill_value=0)
        .cumsum(axis=1)
    )
    return (
        (
            time_cumsum
            / np.arange(1, time_cumsum.shape[1] + 1).reshape(1, -1).repeat(3, axis=0)
        )
        .reset_index()
        .melt(ignore_index=False, value_name="cumsum", id_vars=["agree"])
    )


def preprocess_pie_by_sex(cumsum_radio_data: DataFrame[Dataset]) -> DataFrame[Dataset]:
    return cumsum_radio_data.groupby(["sex", "agree"])["cumsum"].mean().reset_index()


def preprocess_radar_chart_by_sex(
    cumsum_radio_data: DataFrame[Dataset],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    data_by_sex_age = (
        cumsum_radio_data.groupby(["sex", "age", "agree"])["cumsum"]
        .mean()
        .reset_index()
    )
    men_data = data_by_sex_age[data_by_sex_age["sex"] == "男性"]
    women_data = data_by_sex_age[data_by_sex_age["sex"] == "女性"]
    return men_data, women_data


def preprocess_geo_scatter(
    cumsum_radio_data: DataFrame[Dataset],
) -> DataFrame[DatasetWithLonLat]:
    count = (
        cumsum_radio_data.dropna(subset="cumsum", how="any")
        .groupby(["prefecture"])["agree"]
        .count()
        .rename("count")
        .reset_index()
    )
    cumsum_radio_data = cumsum_radio_data[cumsum_radio_data["agree"] == "賛成"]
    cumsum_radio_data_by_city = (
        cumsum_radio_data.dropna(subset="cumsum")
        .groupby(["prefecture", "agree"])["cumsum"]
        .mean()
        .reset_index()
    )
    cumsum_radio_data = cumsum_radio_data_by_city.merge(count, how="left", on="prefecture")
    return cumsum_radio_data.dropna(subset=["count"], how="any")

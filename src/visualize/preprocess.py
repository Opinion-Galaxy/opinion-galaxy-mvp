from typing import Tuple
import pandas as pd
from pandera.typing import DataFrame

from ..data import merge_lonlat
from ..type import DatasetWithLonLat, Topics, Dataset


def preprocess_basic_pie(data: pd.DataFrame, selected_topic: Topics) -> pd.DataFrame:
    return pd.DataFrame(data[selected_topic].value_counts()).reset_index()


def preprocess_time_series_area(cumsum_radio_data: DataFrame[Dataset]) -> pd.DataFrame:
    return (
        cumsum_radio_data.groupby(["response_datetime", "agree"])["cumsum"]
        .mean()
        .reset_index()
    )


def preprocess_pie_by_sex(cumsum_radio_data: DataFrame[Dataset]) -> pd.DataFrame:
    return cumsum_radio_data


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
        .groupby("address")["agree"]
        .count()
        .rename("count")
        .reset_index()
    )
    cumsum_radio_data.loc[cumsum_radio_data["agree"] == "反対", "cumsum"] *= -1
    cumsum_radio_data_by_city = (
        cumsum_radio_data.groupby("address")["cumsum"].mean().reset_index()
    )
    cumsum_radio_data = cumsum_radio_data_by_city.merge(count, how="left", on="address")
    return merge_lonlat(cumsum_radio_data)

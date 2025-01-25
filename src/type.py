from datetime import datetime
import enum
from typing import Dict, Literal

from pandera.typing import Series
import pandera as pa



class Topics(enum.Enum):
    """論点のEnumクラス"""

    外国人労働者の受け入れ拡大 = "外国人労働者の受け入れ拡大"
    子育て支援の充実 = "子育て支援の充実"
    インフラ投資の強化 = "インフラ投資の強化"
    イノベーションの促進 = "イノベーションの促進"
    防衛力の強化 = "防衛力の強化"
    憲法９条の改正 = "憲法９条の改正"
    再生可能エネルギーの導入促進 = "再生可能エネルギーの導入促進"
    エネルギー安全保障の確保 = "エネルギー安全保障の確保"
    日米同盟の廃止 = "日米同盟の廃止"
    教育格差の是正 = "教育格差の是正"
    地域資源の活用 = "地域資源の活用"
    働き方の多様化 = "働き方の多様化"
    労働法制の整備 = "労働法制の整備"
    在宅医療の推進 = "在宅医療の推進"
    介護人材の確保 = "介護人材の確保"
    医療費の持続可能性確保 = "医療費の持続可能性確保"
    サイバーセキュリティの強化 = "サイバーセキュリティの強化"
    電子政府の推進 = "電子政府の推進"


Opinions = Literal["賛成", "中立", "反対"]

OpinionMap = Dict[Literal[1, 0, -1], Opinions]


class Data(pa.DataFrameModel):
    """データのスキーマ"""

    response_datetime: Series[datetime]
    sex: Series[Literal["男性", "女性"]] = pa.Field(isin=["男性", "女性"])
    age: Series[Literal[10, 20, 30, 40, 50, 60, 70, 80, 90]] = pa.Field(
        isin=[10, 20, 30, 40, 50, 60, 70, 80, 90]
    )
    prefecture: Series[str]
    city: Series[str]
    外国人労働者の受け入れ拡大: Series[Opinions] = pa.Field(
        isin=["賛成", "中立", "反対"]
    )
    子育て支援の充実: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    インフラ投資の強化: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    イノベーションの促進: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    防衛力の強化: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    憲法９条の改正: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    再生可能エネルギーの導入促進: Series[Opinions] = pa.Field(
        isin=["賛成", "中立", "反対"]
    )
    エネルギー安全保障の確保: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    日米同盟の廃止: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    教育格差の是正: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    地域資源の活用: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    働き方の多様化: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    労働法制の整備: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    在宅医療の推進: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    介護人材の確保: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    医療費の持続可能性確保: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    サイバーセキュリティの強化: Series[Opinions] = pa.Field(
        isin=["賛成", "中立", "反対"]
    )
    電子政府の推進: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])


class Dataset(pa.DataFrameModel):
    """データセットのスキーマ"""

    response_datetime: Series[datetime]
    sex: Series[Literal["男性", "女性"]] = pa.Field(isin=["男性", "女性"])
    age: Series[
        Literal["10代", "20代", "30代", "40代", "50代", "60代", "70代", "80代"]
    ] = pa.Field(isin=["10代", "20代", "30代", "40代", "50代", "60代", "70代", "80代"])
    address: Series[str]
    agree: Series[Opinions] = pa.Field(isin=["賛成", "中立", "反対"])
    cumsum: Series[float] = pa.Field(ge=0, le=1)


class DatasetWithLonLat(pa.DataFrameModel):
    address: Series[str]
    lon: Series[float] = pa.Field(ge=-180, le=180)
    lat: Series[float] = pa.Field(ge=-90, le=90)
    count: Series[int]
    cumsum: Series[float] = pa.Field(ge=-1, le=1)

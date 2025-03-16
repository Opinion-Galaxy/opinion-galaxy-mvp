import os
import plotly.express as px

opinion_map = {"1": "賛成", "0": "中立", "-1": "反対"}

color_map = {
    "賛成": px.colors.sequential.RdBu_r[2],
    "中立": px.colors.sequential.RdBu_r[4],
    "反対": px.colors.sequential.RdBu_r[-3],
}

figure_tabs = ["意見の推移", "性別の割合", "性別・年代別の割合", "地域別の賛成割合"]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

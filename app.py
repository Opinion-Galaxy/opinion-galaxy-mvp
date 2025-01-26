import pandas as pd
import streamlit as st
import logging

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)
from src.database import get_db_connection, get_topic_instance, get_user_driver_instance, get_comment_driver_instance, get_answer_driver_instance
from src.firebase.auth import logout

from src.components import (
    footer,
    basic_info,
    login,
)
from src.page import (
    dashboard,
    generate_page
)
from src.api import usecase

from src.style import sanitize_style, get_theme_js

pd.set_option("display.max_columns", 100)

logger = logging.getLogger(__name__)

# Initialize cached resources
conn = get_db_connection()
topic_driver = get_topic_instance(conn)
st.session_state.topics = [row["topic"] for row in topic_driver.get_all()]
topics = st.session_state.topics
user_driver, comment_driver, answer_driver = (
    get_user_driver_instance(conn),
    get_comment_driver_instance(conn),
    get_answer_driver_instance(conn),
)

usecase_user, usecase_comment, usecase_answer = (
    usecase.User(user_driver),
    usecase.Comment(comment_driver),
    usecase.Answer(answer_driver),
)
# topics = ['外国人労働者の受け入れ拡大', '子育て支援の充実', 'インフラ投資の強化', 'イノベーションの促進', '防衛力の強化', '憲法９条の改正', '再生可能エネルギーの導入促進', 'エネルギー安全保障の確保', '日米同盟の廃止', '教育格差の是正', '地域資源の活用', '働き方の多様化', '労働法制の整備', '在宅医療の推進', '介護人材の確保', '医療費の持続可能性確保', 'サイバーセキュリティの強化', '電子政府（e-Government）の推進']

################################
# ユーザー基本情報
################################

user_info_page = st.Page(
    lambda: basic_info(usecase_user),
    title="ユーザー情報",
    url_path="user_info",
    icon=":material/account_circle:"
)
login_page = st.Page(lambda: login(usecase_user, user_info_page), title="ログイン", icon=":material/login:")

logout_page = st.Page(logout, title="ログアウト", icon=":material/logout:")


def template_wrapper(selected_topic):
    def template():
        try:
            generate_page(selected_topic, usecase_user, usecase_comment, usecase_answer)
        except Exception as e:
            logger.error(e)
            st.error("エラーが発生しました")
            st.button("リロード", on_click=st.rerun)
        footer()
    return template
pages =[]
for selected_topic in topics:
    pages.append(
         st.Page(template_wrapper(selected_topic), title=selected_topic, url_path=selected_topic, icon=":material/stacked_line_chart:")
    )

dashboard_page = st.Page(
    lambda: dashboard(st.session_state.topics, pages, usecase_answer, usecase_user),
    title="ダッシュボード", 
    icon=":material/dashboard:",
    default=True
)
# if "user" in st.session_state:
#     print(st.session_state.user)
# if "basic_info" in st.session_state:
#     print(st.session_state.basic_info)
# print(st.session_state)
pg = st.navigation(
    {
        "アカウント": [dashboard_page, user_info_page , logout_page],
        "トピック": pages
    } if "user" in st.session_state and st.session_state.user and "basic_info" in st.session_state and st.session_state.basic_info else [
        login_page, user_info_page
    ]
)

st.markdown(sanitize_style, unsafe_allow_html=True)

pg.run()
import pandas as pd
import streamlit as st
import logging

import urllib
import warnings

# ページ設定
st.set_page_config(
    page_title="日本の政治論点ダッシュボード",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)
from streamlit.components.v1 import html
from src.database import get_db_connection, get_topic_instance, get_user_driver_instance, get_comment_driver_instance, get_answer_driver_instance
from src.firebase.auth import logout

from src.components import (
    footer,
    basic_info,
    login,
    forget_password,
    sign_up
)
from src.page import (
    dashboard,
    generate_page
)
from src.api import usecase

from src.style import sanitize_style, get_theme_js

warnings.simplefilter('ignore', FutureWarning)
pd.set_option("display.max_columns", 100)

logger = logging.getLogger(__name__)

html('''
    <script>
        window.top.document.querySelectorAll(`[href*="streamlit.io"]`).forEach(e => e.setAttribute("style", "display: none;"));
    </script>
''')
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
user_info_page = st.Page(
    lambda: basic_info(usecase_user, dashboard_page),
    title="ユーザー情報",
    url_path="user_info",
    icon=":material/account_circle:"
)
login_page = st.Page(lambda: None, title="ログイン", icon=":material/login:", url_path="login")
forget_password_page = st.Page(lambda: forget_password(login_page), title="パスワードを忘れた", icon=":material/password:", url_path="forget_password")
login_page._page = lambda: login(usecase_user, user_info_page, dashboard_page, forget_password_page)
signup_page = st.Page(lambda: sign_up(usecase_user, login_page), title="新規登録", icon=":material/assignment_ind:", url_path="sign_up")

logout_page = st.Page(logout, title="ログアウト", icon=":material/logout:")

if "user_id" in st.query_params:
    user_info = usecase_user.get_user(st.query_params["user_id"])
    if user_info:
        st.session_state.user = {
            "localId": user_info.id,
        }
        st.session_state.basic_info = {
            "user_id": user_info.id,
            "name": user_info.name,
            "age": user_info.age,
            "sex": "男性" if user_info.is_male else "女性",
            "prefecture": user_info.prefecture,
            "city": user_info.city,
        }

pg = st.navigation(
    {
        "アカウント": [dashboard_page, user_info_page , logout_page],
        "トピック": pages
    } if "user" in st.session_state and st.session_state.user and "basic_info" in st.session_state and st.session_state.basic_info else [
        signup_page, login_page, user_info_page, forget_password_page
    ]
)


session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
url = urllib.parse.urlunparse([session.client.request.protocol, session.client.request.host, "", "", "", ""])
from streamlit.components.v1 import html
html('''
<script>
    window.parent.document.querySelectorAll("[data-testid=stLogoLink]").forEach(e => e.setAttribute("target", "_self"));
</script>
''')
st.logo("data/image/logo.png", icon_image="data/image/logo.png", size="large", link=f"{url}" + f"?user_id={st.session_state.basic_info["user_id"]}" if "basic_info" in st.session_state else "")
st.markdown(sanitize_style, unsafe_allow_html=True)

pg.run()
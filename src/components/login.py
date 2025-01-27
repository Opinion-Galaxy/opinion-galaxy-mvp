import re
import streamlit as st
from .. import firebase
from ..style import display_none_style

def validation(email, password):
    if "first_render" not in st.session_state or not st.session_state.first_render:
        st.session_state.first_render = True
        return
    if len(password) == 0:
        st.error("パスワードを入力してください")
        st.rerun()
    if len(password) < 6:
        st.error("パスワードは6文字以上で入力してください")
        st.rerun()
    if len(email) == 0:
        st.error("メールアドレスを入力してください")
        st.rerun()
    if not re.search(r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        st.error("メールアドレスの形式が正しくありません")
        st.rerun()

# @st.dialog("サインイン")
def login(usecase_user, user_info_page, dashboard_page):
    with st.form(key="login-form"):
        email = st.empty()
        email = email.text_input("メールアドレス", placeholder="user@gmail.com")
        password = st.text_input("パスワード", type="password")
        submit = st.form_submit_button("ログイン")
    if submit:
        validation(email, password)
    if submit and firebase.authenticate(email, password):
        st.markdown(
            display_none_style,
            unsafe_allow_html=True,
        )
        st.session_state.first_render = False
        user_info = usecase_user.get_user(st.session_state.user["localId"])
        if user_info is None:
            st.switch_page(user_info_page)
            return

        st.session_state.basic_info = {
            "user_id": user_info.id,
            "name": user_info.name,
            "age": user_info.age,
            "sex": "男性" if user_info.is_male else "女性",
            "prefecture": user_info.prefecture,
            "city": user_info.city
        }
        st.switch_page(dashboard_page)
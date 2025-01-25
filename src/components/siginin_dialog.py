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
    if not re.search("@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        st.error("メールアドレスの形式が正しくありません")
        st.rerun()

@st.dialog("サインイン")
def login_dialog():
    with st.form(key="login-form"):
        email = st.empty()
        email = email.text_input("メールアドレス", placeholder="user@gmail.com")
        password = st.text_input("パスワード", type="password")
        submit = st.form_submit_button("ログイン")
    validation(email, password)
    if submit and firebase.authenticate(email, password):
        st.markdown(
            display_none_style,
            unsafe_allow_html=True,
        )
        st.session_state.first_render = False
        st.rerun()
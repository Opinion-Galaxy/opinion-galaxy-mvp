import streamlit as st
from .. import firebase
from ..style import display_none_style

@st.dialog("サインイン")
def login_dialog():
    with st.form(key="login-form"):
        email = st.empty()
        email = email.text_input("メールアドレス", placeholder="user@gmail.com")
        password = st.text_input("パスワード", type="password")
        submit = st.form_submit_button("ログイン")
    if submit and firebase.authenticate(email, password):
        st.markdown(
            display_none_style,
            unsafe_allow_html=True,
        )
        st.rerun()
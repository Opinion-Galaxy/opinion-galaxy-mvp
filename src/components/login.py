import re

import streamlit as st

from src.data import load_data
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


def on_change_forget_email():
    st.session_state.cache_email = st.session_state["forget-email"]


def forget_password(login_page):
    with st.container(key="forget-password-form", border=True):
        email = st.text_input(
            "メールアドレス",
            placeholder="user@gmail.com",
            key="forget-email",
            on_change=on_change_forget_email,
            value=st.session_state.cache_email
            if "cache_email" in st.session_state
            else "",
        )
        cols = st.columns(2, vertical_alignment="center")
        with cols[0]:
            submit = st.button("パスワードをリセット")
        with cols[1]:
            if (
                "cache_email" not in st.session_state
                or st.session_state.cache_email == ""
            ):
                st.session_state.cache_email = email
            st.page_link(login_page, label="ログイン画面に戻る")
    if submit:
        if firebase.forget_password(email):
            st.success("パスワードリセットのためのメールを送信しました")
        else:
            st.error("メールアドレスが登録されていません")


def on_change_email():
    st.session_state.cache_email = st.session_state["email"]


sign_up_style = """
<style>
    div[class*='st-key-sign-up-form'] .stHorizontalBlock:last-child .stColumn:first-child,  div[class*='st-key-sign-up-form'] .stHorizontalBlock:last-child .stColumn:first-child * {
        width: fit-content !important;
        flex-grow: 0;
        flex-basis: fit-content;
    }
</style>
"""


def sign_up(usecase_answer, usecase_user, login_page):
    st.markdown(sign_up_style, unsafe_allow_html=True)
    with st.container(key="sign-up-form", border=True):
        email = st.text_input(
            "メールアドレス",
            placeholder="user@gmail.com",
            key="email",
            on_change=on_change_email,
            value=st.session_state.cache_email
            if "cache_email" in st.session_state
            else "",
        )
        password = st.text_input(
            "パスワード", type="password", max_chars=16, key="signup_password"
        )
        check_password = st.text_input(
            "パスワード（確認用）",
            type="password",
            max_chars=16,
            key="signup_password_for_check",
        )
        if password != check_password:
            st.error("パスワードが一致しません")
        cols = st.columns(2, vertical_alignment="center")
        with cols[0]:
            submit = st.button("新規登録")
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
                st.success(
                    "ご登録のメールアドレスに確認メールを送信しました。メール内のリンクをクリックして登録を完了してください"
                )
                cols = st.columns(2, vertical_alignment="center")
                st.page_link(login_page, label="ログイン画面に戻る")
                return
            st.error("すでに登録されているメールアドレスです")
        with cols[1]:
            if (
                "cache_email" not in st.session_state
                or st.session_state.cache_email == ""
            ):
                st.session_state.cache_email = email
            st.page_link(login_page, label="アカウントをお持ちの方はこちら")

    load_data(usecase_answer, usecase_user)


login_style = """
<style>
    div[class*='st-key-login-form'] .stHorizontalBlock:last-child .stColumn:first-child,  div[class*='st-key-login-form'] .stHorizontalBlock:last-child .stColumn:first-child * {
        width: fit-content;
        flex-grow: 0;
        flex-basis: fit-content;
    }
</style>
"""


def login(
    usecase_answer, usecase_user, user_info_page, dashboard_page, forget_password_page
):
    st.markdown(login_style, unsafe_allow_html=True)
    with st.container(key="login-form", border=True):
        email = st.text_input(
            "メールアドレス",
            placeholder="user@gmail.com",
            key="email",
            on_change=on_change_email,
            value=st.session_state.cache_email
            if "cache_email" in st.session_state
            else "",
        )
        password = st.text_input("パスワード", type="password")
        cols = st.columns(2, vertical_alignment="center")
        with cols[0]:
            submit = st.button("ログイン")
        with cols[1]:
            if (
                "cache_email" not in st.session_state
                or st.session_state.cache_email == ""
            ):
                st.session_state.cache_email = email
            st.page_link(forget_password_page, label="パスワードを忘れた方はこちら")
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
            "city": user_info.city,
        }
        st.switch_page(dashboard_page)
    load_data(usecase_answer, usecase_user)

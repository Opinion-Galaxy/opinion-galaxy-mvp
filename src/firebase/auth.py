import json
import logging
import pyrebase
import requests
import streamlit as st
from .config import firebaseConfig as cfg


logger = logging.getLogger(__name__)
firebase = pyrebase.initialize_app(cfg)
auth = firebase.auth()

def authenticate(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.session_state.user = user
        return True

    except requests.exceptions.HTTPError as e:
        msg = json.loads(e.args[1])["error"]["message"]
        if msg != "EMAIL_EXISTS":
            logger.error(e, msg)
            st.error("ユーザーの作成に失敗しました")
        else:
            if login(email, password):
                return True

        if "user" in st.session_state:
            del st.session_state.user
    return False

def login(email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            return True

        except requests.exceptions.HTTPError as e:
            msg = json.loads(e.args[1])["error"]["message"]
            if msg == "EMAIL_NOT_FOUND" or msg == "INVALID_PASSWORD":
                st.error("メールアドレスかパスワードに誤りがあります。")
            elif msg == "USER_DISABLED":
                st.error("このユーザーは無効化されています。管理者にお問い合わせください。")
            elif msg == "TOO_MANY_ATTEMPTS_TRY_LATER":
                st.error("試行回数が多すぎます。しばらく経ってからお試しください。")
            else:
                logger.error(e)
            return False

def logout():
    auth.current_user = None
    del st.session_state.user

def refresh():
    if "user" not in st.session_state:
        return False
    try:
        user = auth.refresh(st.session_state.user["refreshToken"])
        st.session_state.user = user
        return True
    except Exception:
        del st.session_state.user
    return False
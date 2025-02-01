import json
import logging
import re
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
        auth.send_email_verification(user["idToken"])
        st.session_state.user = user
        return True

    except requests.exceptions.HTTPError as e:
        msg = json.loads(e.args[1])["error"]["message"]
        if msg == "EMAIL_EXISTS":
            if login(email, password):
                return True
        elif "PASSWORD_DOES_NOT_MEET_REQUIREMENTS" in msg:
            error_msgs = []
            if "Password must contain at least" in msg:
                re.search(r"(\d+)", msg)
                error_msgs.append(f"{re.search(r'at\s+least\s*(\d+)', msg).group(1)}文字以上で")
            if "Password may contain at most" in msg:
                error_msgs.append(f"{re.search(r'at\s+most\s*([0-9]+)', msg).group(1)}文字以下で")
            if "Password must contain an upper case character" in msg:
                error_msgs.append("大文字のアルファベット")
            if "Password must contain a lower case character" in msg:
                error_msgs.append("小文字のアルファベット")
            if "Password must contain a numeric character" in msg:
                error_msgs.append("数字")
            if error_msgs:
                error_msg = '、'.join(error_msgs)
                st.error(f"パスワードは{error_msg if error_msg.endswith("以上") or error_msg.endswith("以下") else error_msg +  "を含めて"}入力してください")
        else:
            logger.error(e, msg)
            st.error("ユーザーの作成に失敗しました")

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
            if msg == "EMAIL_NOT_FOUND" or msg == "INVALID_PASSWORD" or msg == "INVALID_LOGIN_CREDENTIALS":
                st.error("メールアドレスかパスワードに誤りがあります。")
            elif msg == "USER_DISABLED":
                st.error("このユーザーは無効化されています。管理者にお問い合わせください。")
            elif msg == "TOO_MANY_ATTEMPTS_TRY_LATER":
                st.error("試行回数が多すぎます。しばらく経ってからお試しください。")
            else:
                logger.error(msg)
                logger.error(e)
            return False

def forget_password(email):
    try:
        auth.send_password_reset_email(email)
        st.success("パスワードリセットのためのメールを送信しました")
        return True
    except requests.exceptions.HTTPError as e:
        msg = json.loads(e.args[1])["error"]["message"]
        if msg == "EMAIL_NOT_FOUND":
            st.error("このメールアドレスは登録されていません")
        else:
            logger.error(msg)
            logger.error(e)
        return False

def logout():
    auth.current_user = None
    del st.session_state.user
    st.rerun()

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
import streamlit as st
from src.const import (
    prefecture_list,
    city_dict,
)


@st.dialog("基本情報の入力")
def basic_info_dialog(usecase_user):
    name = st.text_input("ユーザー名", placeholder="ギャラクシー太郎")
    age = st.number_input("年齢", min_value=0, max_value=100, value=30)
    sex = st.radio(
        "性別",
        ["女性", "男性"],
        horizontal=True,
    )
    prefecture = st.selectbox("都道府県", prefecture_list, index=12)
    city = st.selectbox("市区町村", city_dict[prefecture])
    if st.button("送信"):
        with st.spinner("情報を登録中..."):
            user_id = usecase_user.create_user(name, age, sex, prefecture + city)
            st.session_state.basic_info = {
                "user_id": user_id,
                "name": name,
                "age": age,
                "sex": sex,
                "address": prefecture + city,
            }
            st.rerun()

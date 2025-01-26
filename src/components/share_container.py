from typing import Literal
import streamlit as st
from streamlit_javascript import st_javascript
import base64
from ..style import get_theme_js
import urllib.parse
from streamlit_theme import st_theme


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def share_container(selected_topic):
    st.subheader("共有")
    theme = st_javascript(get_theme_js)
    # theme = 'light'
    session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
    url = urllib.parse.urlunparse([session.client.request.protocol, session.client.request.host, "", "", "", ""]) + "/" + selected_topic

    with st.container(border=True, key="share-container"):
        cols = st.columns(4, vertical_alignment="center")
        with cols[0]:
            st.markdown(
                f'''
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw&text={url}" class="twitter-share-button" data-show-count="false">
                    <img width="30" src="data:image/svg+xml;base64,{get_base64_of_bin_file("data/image/X.svg" if theme == "light" else "data/image/X_white.svg")}" />
                </a>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                ''',
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(f'''
                <a href="http://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="nofollow noopener noreferrer">
                    <img src="data:image/svg+xml;base64,{get_base64_of_bin_file("data/image/Facebook.svg" if theme == "light" else "data/image/Facebook_white.svg")}" />
                </a>
            ''', unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f'''
                         <a target="_blank" href="https://tiktok.com/" target="_blank" rel="nofollow noopener noreferrer">
                            <img src="data:image/svg+xml;base64,{get_base64_of_bin_file("data/image/Tik Tok.svg")}" />
                         </a>
                         ''', unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f'''
                         <a target="_blank" href="https://instagram.com/" target="_blank" rel="nofollow noopener noreferrer">
                            <img src="data:image/svg+xml;base64,{get_base64_of_bin_file("data/image/Instagram.svg")}" />
                         </a>
                         ''', unsafe_allow_html=True)

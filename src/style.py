display_none_style = """
                <style>
                    div[data-testid="stDialog"] {
                        display: none;
                    }
                </style>
            """

get_theme_js = """window.getComputedStyle(window.parent.document.getElementsByClassName('stApp')[0]).getPropertyValue('color-scheme');"""

sanitize_style = """
    <style>
    /* rem設定 */
    html {
        font-size: 15px;
    }
    p, ol, ul, dl {
        margin: 0px 0px 1rem;
        padding: 0px;
        font-size: 1rem;
        font-weight: 400;
    }
    /* st_javascriptのiframeを非表示にする */
    div:has(> iframe[title='streamlit_javascript.streamlit_javascript']) {
        display: none !important;
    }
    /* ページの幅が640px以下の場合、stColumnのmin-widthを解除する */
    @media (max-width: 640px) {
        .stColumn {
            min-width: unset;
        }
    }
    .stColumn div {
        margin: 0;
    }
    .stColumn p {
        margin: 0;
    }

    </style>
"""

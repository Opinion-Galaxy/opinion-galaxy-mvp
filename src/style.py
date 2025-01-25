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
    p, ol, ul, dl {
        margin: 0px;
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
        justify-items: center;
        margin: 0;
    }
    </style>
"""

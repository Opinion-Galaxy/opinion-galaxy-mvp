display_none_style = """
                <style>
                    div[data-testid='stDialog'] {
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
    /* divider余白設定 */
    html body .stMarkdown > div > hr {
        margin: 0;
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
    .stMainBlockContainer > div > div > .stVerticalBlock > stElementContainer:nth-child(n+1):not(-n+3) {
        margin: -1rem;
    }
    .stColumn div {
        margin: 0;
    }
    .stColumn p {
        margin: 0;
    }
    div:has(+ img.stLogo) {
        mix-blend-mode: exclusion;
    }
    img.stLogo {
        max-width: unset;
        height: 2.5rem;
        margin: 0;
    }
    div[data-testid="stSidebarCollapsedControl"] {
        top: 1.2rem;
    }
    div[data-testid="stSidebarHeader"] {
        padding-top: 1.2rem;
    }
    iframe {
        display: none;
    }
    div.stElementContainer:has(iframe), div.stElementContainer:has(div.stMarkdown > div > style) {
        margin: -1rem 0 0 0;
    }
    </style>
"""

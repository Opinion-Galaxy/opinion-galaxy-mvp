import streamlit as st
import pandas as pd
import plotly.express as px

from src.predict import predict
from src.predict import create_dataset


def election_predict():
    st.markdown(
        """
    <style>
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock > .stColumn:first-child {
            flex-basis: 120px;
            width: 120px;
            flex-grow: 0;
            text-align: center;
            margin-left: 0.5rem;
        }
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock {
            gap: 2.5rem;
        }
        div[class*="st-key-candidate_card_"] .stHorizontalBlock {
            flex-wrap: nowrap;
        }
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock > div:nth-child(2) > div > div > div > div:nth-child(1) > div:nth-child(1) > div > div > div > div > div > div > p {
            border: 1px solid;
            border-radius: 20px;
            line-break: strict;
            padding: 0.1rem 0.4rem;
            text-align: center;
            font-size: 0.8rem;
        }
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock > div:nth-child(2) > div > div > div > div:nth-child(1) > .stColumn:nth-child(1) {
            width: fit-content;
            flex-grow: 0;
            flex-basis: fit-content;
            margin: 0;
        }
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock > div:nth-child(2) > div > div > div > div:nth-child(1) > .stColumn:nth-child(1) * {
            width: fit-content !important;
            flex-grow: 0;
            flex-basis: fit-content;
        }
        div[class*="st-key-candidate_card_"] > .stHorizontalBlock > div:nth-child(2) > div > div > div > div:nth-child(2) * {
            width: fit-content !important;
            flex-grow: 0;
            flex-basis: fit-content;
        }
        .自由民政党 {
            color: rgb(210, 35, 25);
            border-color: rgb(210, 35, 25);
        }
        .立憲民主フォーラム{
            color: rgb(35, 145, 255);
            border-color: rgb(35, 145, 255);
        }
        .日本共和党 {
            color: rgb(110, 65, 225);
            border-color: rgb(110, 65, 225);
        }
        .進歩未来党 {
            color: rgb(182, 200, 27);
            border-color: rgb(182, 200, 27);
        }
        .日本改革の会 {
            color: rgb(225, 154, 0);
            border-color: rgb(225, 154, 0);
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.write(
        """
        <h2>選挙予測<span style="font-size: 12px;">※</span></h2>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("第100回衆議院選挙")
    st.write(
        """
            <p style="
                text-align: center;
                font-size: 24px;
            ">東京31区</p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    dummy_election = st.cache_data(pd.read_csv)("data/dummy_election.csv")
    dummy_election_1 = dummy_election[dummy_election["選挙区"] == "1区"]
    dataset = create_dataset(dummy_election)
    X_test, y_test = (
        dataset[dummy_election["選挙区"] == "1区"].drop(columns=["得票率", "選挙区"]),
        dataset[dummy_election["選挙区"] == "1区"]["得票率"],
    )
    pred = predict(X_test, y_test)
    dummy_election_1["得票率"] = pred
    dummy_election_1 = dummy_election_1.sort_values("得票率", ascending=False)
    with st.container():
        for i, candidate_row in dummy_election_1.iterrows():
            with st.container(key=f"candidate_card_{i}", border=True):
                card_cols = st.columns(2, vertical_alignment="center")
                with card_cols[0]:
                    st.image(f"data/image/candidate_{i + 1}.jpg", width=120)
                with card_cols[1]:
                    name_cols = st.columns(2)
                    with name_cols[0]:
                        st.write(
                            f"""
                            <p class="{candidate_row["所属"].split("(")[0]}">
                                {candidate_row["所属"].split("(")[0].replace("党", "").replace("の会", "").replace("フォーラム", "")}
                            </p>
                            """,
                            unsafe_allow_html=True,
                        )
                    with name_cols[1]:
                        st.write(candidate_row["候補者名"])
                    info_cols = st.columns(3)
                    with info_cols[0]:
                        st.write(f"{candidate_row['年齢']}歳")
                    with info_cols[1]:
                        st.write(f"{candidate_row['性別']}")
                    st.write(candidate_row["経歴・特徴"])
                with st.container():
                    fig = px.bar(
                        pd.Series(candidate_row["得票率"]),
                        labels={"value": "得票率", "index": "", "variable": ""},
                        hover_data={"value": ":.1f}%"},
                        orientation="h",
                        height=64,
                    )
                    fig.update_traces(marker_color="#f50909")
                    fig.update_layout(
                        yaxis=dict(
                            tickvals=[0],
                            ticktext=[f"{candidate_row['候補者名']}"],
                            showticklabels=False,
                            title=None,
                        ),
                        xaxis=dict(
                            range=[0, 100],
                            tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                            ticktext=[
                                "0%",
                                "10%",
                                "20%",
                                "30%",
                                "40%",
                                "50%",
                                "60%",
                                "70%",
                                "80%",
                                "90%",
                                "100%",
                            ],
                            title=None,
                        ),
                        margin=dict(l=0, r=0, t=0, b=0, pad=0),
                        showlegend=False,
                    )
                    st.plotly_chart(fig, config={"displayModeBar": False})
                    st.write(
                        f"""<p style="text-align: center; font-size: 18px">得票率:&emsp;<span style="font-weight: bold; font-size: 28px;">{candidate_row["得票率"]:.1f}%<span></p>""",
                        unsafe_allow_html=True,
                    )
    st.write(
        "※ この予測は機械学習モデルによるものであり、実際の選挙結果と異なる場合があります。"
    )

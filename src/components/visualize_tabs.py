import streamlit as st

from src.const import figure_tabs
from src.data import create_dataset
from src.visualize import visualize_data_by_various_method


async def visualize_tabs(data, selected_topic):
    tabs = st.tabs(figure_tabs)
    cumsum_radio_data = create_dataset(data, selected_topic)
    await visualize_data_by_various_method(tabs, cumsum_radio_data)

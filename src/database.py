import sqlite3
import streamlit as st

from src.api import driver


# -------------------
# Cached Database Connection
# -------------------
@st.cache_resource(hash_funcs={str: lambda x: x})
def get_db_connection(db_path="data/database/database.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------
# Cached Class Instances
# -------------------
@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_user_driver_instance(conn: sqlite3.Connection):
    return driver.User(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_comment_driver_instance(conn):
    return driver.Comment(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_answer_driver_instance(conn):
    return driver.Answer(conn)


@st.cache_resource(hash_funcs={sqlite3.Connection: id})
def get_topic_instance(conn):
    return driver.Topic(conn)

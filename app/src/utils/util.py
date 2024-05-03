import logging
import streamlit as st
import psycopg2

# logging boilerplate
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
rootLogger = logging.getLogger()

# Create a postgres connection to pass to different pages
conn = psycopg2.connect(host='postgres', port=5432, database='postgres', user=st.secrets['postgres']['username'], password=st.secrets['postgres']['password'])
conn.autocommit = True
database_cursor = conn.cursor()

def halt_error(msg: str):
    """
    Logs an error message and then halts the execution of a streamlit page.

    Args:
        msg (str): Message to log
    """
    rootLogger.error(msg)
    st.error(msg)
    st.stop()


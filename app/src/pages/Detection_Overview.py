import streamlit as st
import psycopg2
import pandas as pd
import logging
from utils.util import halt_error, database_cursor

logger = logging.getLogger()


#----- Streamlit Page Configuration -----#
st.set_page_config(
    page_title='Detection Overview',
    page_icon="random"
)

# Error if we don't have any configured tools
try:
    if len(st.session_state["selected_tools"]) == 0:
        halt_error('No Tool Configured! Head back to Overview')
except KeyError:
    halt_error('No Tool Configured! Head back to Overview')


with st.sidebar:
    # Get listing of detections per platform
    st.sidebar.text('Tools')
    tools = st.selectbox('Platform Selection',st.session_state["selected_tools"])
    # Get all detections where the tool is equal to the sidebar selected tool
    sql = """SELECT name, logic FROM test_table WHERE tool=%s;"""
    database_cursor.execute(sql, (tools,))
    df = pd.DataFrame(database_cursor.fetchall(), columns=[desc[0] for desc in database_cursor.description])

st.write(df)


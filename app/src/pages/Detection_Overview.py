import streamlit as st
import psycopg2
import pandas as pd
import logging
from utils.util import halt_error, database_cursor
from utils.splunk import get_alerts
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
    if "Splunk" in st.session_state["selected_tools"]:
        searches = get_alerts(st.secrets['splunk']['username'], st.secrets['splunk']['password'], st.secrets['splunk']['base_url'])
        st.write(searches)
    # Get all detections where the tool is equal to the sidebar selected tool
    sql = """SELECT * FROM detections WHERE tool=%s;"""
    database_cursor.execute(sql, (tools,))
    df = pd.DataFrame(database_cursor.fetchall(), columns=[desc[0] for desc in database_cursor.description])

st.write(df)


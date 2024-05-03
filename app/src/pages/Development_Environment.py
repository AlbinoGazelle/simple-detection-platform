import streamlit as st
import psycopg2
import requests
from utils.util import rootLogger, halt_error, database_cursor




def test_splunk_connection(username: str, password: str, url: str):
    """
    Tests connection to Splunk via `services/authentication/current-context` endpoint.\n
    Args:
        username: Username to authenticate to Splunk.
        password: Password to authenticate to Splunk.
        url: URL to Splunk instance.
    Returns:
        `True` if authentication is successful. `False` if unsuccessful. 
    """
    try:
        response = requests.get(
            f'{url}/services/authentication/current-context',
            verify=False,
            auth=(username, password),
            timeout=100
        )
    except requests.exceptions.ReadTimeout:
        rootLogger.warn('Connection Timeout when connecting to Splunk')
        return False
    if response.status_code in range(200, 208): 
        return True
    else:
        rootLogger.warn(f'Response from Splunk outside of acceptable range:\n {response.text}')
        return False
        

#----- Streamlit Page Configuration -----#
st.set_page_config(
    page_title='Development Environment',
    page_icon="random"
)

# Test connection to Splunk, if no connection we can't deploy detections
connection_status = test_splunk_connection(st.secrets['splunk']['username'], st.secrets['splunk']['password'], st.secrets['splunk']['base_url'])

if connection_status == False:
    halt_error(f'Failed to connect to Splunk.')

#----- Create Detection Environment Form -----#
with st.form('detection_environment'):
    st.header('Development Environment')

    detection_name = st.text_input('Detection Name')
    detection_logic = st.text_area('Detection Logic')
    try:
        detection_tool = st.selectbox('Tool', st.session_state["selected_tools"])
    except KeyError:
        st.error('No Tool Configuration Found')

    submit_button = st.form_submit_button('Submit')

    if submit_button:
        sql = """INSERT INTO test_table VALUES (%s, %s, %s);"""
        database_cursor.execute(sql, (detection_name,detection_logic,detection_tool))
        st.write('**Name:**', detection_name, '**Logic:**', detection_logic, '**Tool:**', detection_tool)



    
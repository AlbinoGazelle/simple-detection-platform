import streamlit as st
from utils.util import halt_error, database_cursor
from utils.splunk import test_splunk_connection, create_alert

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
    detection_description = st.text_area('Detection Description')
    try:
        detection_tool = st.selectbox('Tool', st.session_state["selected_tools"])
    except KeyError:
        st.error('No Tool Configuration Found')

    submit_button = st.form_submit_button('Submit')

    if submit_button:
        sql = """INSERT INTO detections (name, logic, description, tool) VALUES (%s, %s, %s, %s);"""
        database_cursor.execute(sql, (detection_name, detection_logic, detection_description, detection_tool))
        if detection_tool == 'Splunk':
            create_alert(st.secrets['splunk']['username'], st.secrets['splunk']['password'], st.secrets['splunk']['base_url'], detection_name, detection_description, detection_logic)



    
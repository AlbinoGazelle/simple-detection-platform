import streamlit as st
from utils.util import rootLogger

# Configure Page Title and Icon
st.set_page_config(
    page_title="Simple Detection Platform",
    # Random Emoji for icon
    page_icon="random"
)



# Set Sidebar
with st.sidebar:
    # Configure settings for each platform
    st.sidebar.text('Configuration')
    tools = st.multiselect('Platform Selection',['Splunk'])
    st.session_state["selected_tools"] = tools
    secrets_file_usage = None
    
    if 'Splunk' in tools:
        if "splunk" in st.secrets:
            # Skip manual entry of secrets if we have a Splunk entry in .streamlit/secrets.toml
            rootLogger.info('Found secrets.toml. Skipping manual entry of secrets.')
            st.session_state["splunk_url"] = st.secrets["splunk"]["base_url"]
            st.session_state["splunk_user"] = st.secrets["splunk"]["username"]
            st.session_state["splunk_password"] = st.secrets["splunk"]["password"]
            secrets_file_usage = True
            pass
        else:
            # ask user for credentials
            secrets_file_usage = False
            st.session_state["splunk_url"] = st.text_input(
                "Enter the URL for your Splunk server"
            )
            st.session_state["splunk_user"] = st.text_input(
                "Enter the username of your Splunk Service Account"
            )
            st.session_state["splunk_password"] = st.text_input(
                "Enter the URL for your Splunk server",
                type="password"
            )


# Set Overview Introduction

# Create dynamic message based on secrets_file_usage
messages = {
    'nosecrets': "Since you've already configured credentials via .streamlit/secrets.toml you can skip this step!",
    'secrets': "Enter the required configuration information such as username, password, and URL."
}

if secrets_file_usage:
    message = messages['secrets']
else:
    message = messages['nosecrets']

st.markdown(f"""
            # Simple Detection Platform

            ###### Welcome to a simple platform for managing, deploying, and testing security detections across multiple platforms.

            ### Getting Started
            1. Select the security platform(s) you'd like to manage under **Platform Selection** in the sidebar.
            2. {message}
            3. Head over to the `Development Environment` page to start deploying detections!
            """)


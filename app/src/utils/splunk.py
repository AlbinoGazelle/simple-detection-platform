import requests.packages
from utils.util import rootLogger
import requests
from urllib3.exceptions import InsecureRequestWarning
# Disable SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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

def create_alert(username: str, password: str, url: str, detection_name: str, detection_description: str, detection_logic: str):
    """
    Creates an alert in Splunk via `/services/saved/searches/` endpoint

    Args:
        username (str): Username to authentication to Splunk
        password (str): Password to authentication to Splunk
        url (str): URL to Splunk instance
        detection_name (str): name of the alert
        detection_logic (str): logic for the alert
    Returns:
        `True` if creation is successful. `False` if unsuccessful.
    """
    data = {
        'name': detection_name,
        'search': detection_logic,
        'cron_schedule': '*/3 * * * *',
        'description': detection_description,
        'dispatch.earliest_time': '-24h@h',
        'dispatch.latest_time': 'now'
    }
    response = requests.post(f'{url}/services/saved/searches/', data=data, verify=False, auth=(username, password))
    if response.status_code in range(200, 208):
        return True
    else:
        rootLogger.warn(f'Response from Splunk outside of acceptable range:\n {response.text}')
        return False

def get_alerts(username: str, password: str, url: str):
    params = {
        'output_mode': 'json'
    }
    
    response = requests.get(
        f'{url}/services/saved/searches',
        params=params,
        verify=False,
        auth=(username, password)
    )
    response = response.json()
    searches = response["entry"]
    rootLogger.info('Getting all alerts in Splunk')
    cleaned_alerts = []
    for alerts in searches:
        alerts = {key: alerts[key] for key in alerts if key in ['name', 'content','author']}
        alerts['content'] = {key: alerts['content'][key] for key in alerts['content'] if key in ['search', 'description']}
        alerts['name'] = alerts['name']
        alerts['logic'] = alerts['content']['search']
        alerts['tool'] = 'Splunk - Manually Deployed'
        alerts['description'] = alerts['content']['description']
        del alerts['content']
        del alerts['name']
        del alerts['author']
        cleaned_alerts.append(alerts)
    return cleaned_alerts 
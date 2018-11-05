# -*- coding: utf-8 -*-
"""Example python client for connecting with the spot-on.energy forecasting API.

The forecasting API is secured using oauth2 with client credentials flow. The code below demonstrates how to obtain
an access token and use this to make requests.
"""

import requests
from os import getenv

client_id = getenv("CLIENT_ID", "CLIENT_ID_HERE_ON_IN_ENVIRONMENT_VARIABLE")
client_secret = getenv("CLIENT_SECRET", "CLIENT_SECRET_HERE_ON_IN_ENVIRONMENT_VARIABLE")
auth_url = "https://spot-on.eu.auth0.com/oauth/token"

host = "https://api.spot-on.energy"
endpoint = "{}/v1/forecasts".format(host)

# Request auth token
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'audience': host,
    'grant_type': 'client_credentials'
}
response = requests.post(auth_url, json=payload)

# Make a request using auth token
headers = {
    'Authorization': 'Bearer {}'.format(response.json()['access_token'])
}

params = {
    'markets': 'EPEX_NL_DAY_AHEAD'#,
    #'startdate': 'yyyy-mm-dd',
    #'enddate': 'yyyy-mm-dd'
}


response = requests.get(endpoint, headers=headers, params=params)
response.raise_for_status()
print(response.text)
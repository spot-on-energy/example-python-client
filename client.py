# -*- coding: utf-8 -*-
"""Example python client for connecting with the spot-on.energy forecasting API.

The forecasting API is secured with [HMAC Signature authentication](https://tools.ietf.org/html/draft-cavage-http-signatures-10).
The code below demonstrates how to create valid request headers in order to access the data from the API.
"""

import requests
from auth import generate_request_headers
import os

# Retrieve credentials from environment variables.
username = os.getenv('USERNAME')
secret = os.getenv('SECRET')

url = 'https://api.spot-on.energy/v1/forecasts'

# Set the query parameters. Depending on your subscription, these might be restricted.
# See https://spot-on.energy/#products.
query_params = {'markets' : 'EPEX_NL_DAY_AHEAD',
                'days'    : 1}

# Generate the request headers. The header fields that are used are *Authorization* and *Date*.
# The hmac signature is included in the *Authorization* field.
get_request_headers = generate_request_headers(username, secret, url, query_params)

# An example request
r = requests.get(url, headers=get_request_headers, params=query_params)

# Verify that the response is ok and print the result.
print('Response code: {}\n'.format(r.status_code))
print(r.text)
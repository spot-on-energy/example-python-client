import requests
from auth import generate_request_headers
import os

key_id = os.getenv('USERNAME', 'test')
secret = os.getenv('SECRET', 'test')
url = 'https://dev-kong.spot-on.energy/v1/forecasts'

query_params = {'markets' : 'EPEX_NL_DAY_AHEAD',
                'days'    : 1}

get_request_headers = generate_request_headers(key_id, secret, url, query_params)

r = requests.get(url, headers=get_request_headers, params=query_params, verify=False)

print('Response code: {}\n'.format(r.status_code))
print(r.text)
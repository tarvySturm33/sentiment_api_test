from dotenv import load_dotenv
from datetime import datetime as dt
import os
import requests

class RequestBuilder:

    def __init__(self, host='ip-172-31-41-72', port=8000):
        self.host = host
        self.port = port

    def build_url(self, endpoint):
        return f'http://{self.host}:{self.port}{endpoint}'

    def get(self, endpoint, params=None):
        url = self.build_url(endpoint)
        return requests.get(url=url, params=params)

# date format
dt_ft = '%Y-%m-%d %H:%M:%S.%f'

# load variables of the target environment (test)

load_dotenv()

api_host = os.environ.get('HOST', 'ip-172-31-41-72')
api_port = os.environ.get('PORT', 8000)

# instantiate request builder

request_builder = RequestBuilder(
    host=api_host,
    port=api_port
)

# test dataset
test_data = [
    {
        'username': 'alice',
        'password': 'wonderland',
        'entries': [
            {'target': '/v1', 'expected_code': 200},
            {'target': '/v2', 'expected_code': 200}
            ]
    },
    {
        'username': 'bob',
        'password': 'builder',
        'entries': [
            {'target': '/v1', 'expected_code': 200},
            {'target': '/v2', 'expected_code': 403}
            ]
    }
]

# endpoint to test
endpoint = '{}/sentiment'

for user in test_data:
    for entry in user['entries']:
        target = entry['target']
        response = request_builder.get(
            endpoint=endpoint.format(target),
            params={
                'username': user['username'],
                'password': user['password']
            }
        )
        output = '''
        ============================
            Authorization test
        ============================

        request done to "{endpoint}" at {timestamp}

        | username= {usr}
        | password= {pwd}
        expected result = {expected_code}
        actual result = {status_code}
        ==>  {test_status}
        '''
        # query status
        status_code = response.status_code
        # display the results
        if status_code == entry['expected_code']:
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'
        output = output.format(status_code=status_code,
                               test_status=test_status,
                               expected_code=entry['expected_code'],
                               usr=user['username'],
                               pwd=user['password'],
                               endpoint=endpoint.format(target),
                               timestamp=dt.now().strftime(dt_ft)[:-3])
        # printing in a file
        if os.environ.get('LOG') == '1':
            with open('api_test.log', 'a') as file:
                file.write(output)
        else:
            print(output)

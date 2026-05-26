from dotenv import load_dotenv
from datetime import datetime as dt
import os
import requests

class RequestBuilder:

    def __init__(self, host='localhost', port=8000):
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

api_host = os.environ.get('HOST','localhost')
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
            {
                'target': '/v1',
                'sentence': 'life is beautiful',
                'expected_positive': True
                },
            {
                'target': '/v2',
                'sentence': 'life is beautiful',
                'expected_positive': True
                },
            {
                'target': '/v1',
                'sentence': 'that sucks',
                'expected_positive': False
                },
            {
                'target': '/v2',
                'sentence': 'that sucks',
                'expected_positive': False
                },
            ]
    }
]

# endpoint to test
endpoint = '{}/sentiment'

for user in test_data:
    for entry in user['entries']:
        target = entry['target']
        score = 'positive' if entry['expected_positive'] else 'negative'
        response = request_builder.get(
            endpoint=endpoint.format(target),
            params={
                'username': user['username'],
                'password': user['password'],
                'sentence': entry['sentence']
            }
        )
        output = '''
        ============================
            Content test
        ============================

        request done to "{endpoint}" at {timestamp}

        | username= {usr}
        | password= {pwd}
        expected result = {score}
        actual result = {actual_score}
        ==>  {test_status}
        '''
        # query status
        data = response.json()
        result_positive = data['score'] > 0
        # display the results
        if result_positive == entry['expected_positive']:
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'
        output = output.format(actual_score=data['score'],
                               score=score,
                               test_status=test_status,
                               usr=user['username'],
                               pwd=user['password'],
                               endpoint=endpoint.format(target),
                               timestamp=dt.now().strftime(dt_ft)[:-3])
        # printing in a file
        if os.environ.get('LOG') == '1':
            with open('/api_test.log', 'a') as file:
                file.write(output)
        else:
            print(output)

from dotenv import load_dotenv
from datetime import datetime as dt
import os

from RequestBuilder import RequestBuilder

# date format
dt_ft = '%Y-%m-%d %H:%M:%S.%f'

# load variables of the target environment (test)

load_dotenv()

api_host = os.environ.get('HOST', '0.0.0.0')
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
        'expected_code': 200
    },
    {
        'username': 'bob',
        'password': 'builder',
        'expected_code': 200
    },
    {
        'username': 'clementine',
        'password': 'mandarine',
        'expected_code': 403
    }
]

# endpoint to test
endpoint = '/permissions'

for user in test_data:
    response = request_builder.get(
        endpoint=endpoint,
        params={
            'username': user['username'],
            'password': user['password']
        }
    )
    output = '''
    ============================
        Authentication test
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
    if status_code == user['expected_code']:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    output = output.format(status_code=status_code,
                           test_status=test_status,
                           expected_code=user['expected_code'],
                           usr=user['username'],
                           pwd=user['password'],
                           endpoint=endpoint,
                           timestamp=dt.now().strftime(dt_ft)[:-3])
    # printing in a file
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            file.write(output)
    else:
        print(output)

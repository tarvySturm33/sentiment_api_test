from dotenv import load_dotenv
import os
import requests
# definition of the API's params

load_dotenv()
api_host = os.environ.get('HOST', '0.0.0.0')
api_port = os.environ.get('PORT', 8000)

test_data = [
    {'username': 'alice',
     'password': 'wonderland',
     'expected_code': 200},
    {'username': 'bob',
     'password': 'builder',
     'expected_code': 200},
    {'username': 'clementine',
     'password': 'mandarine',
     'expected_code': 403}
    ]

for user in test_data:
    r = requests.get(url='http://{address}:{port}/permissions'.
                     format(address=api_host, port=api_port),
                     params={
                         'username': user['username'],
                         'password': user['password']
                         })
    output = '''
    ============================
        Authentication test
    ============================
    request done at "/permissions"
    | username= {usr}
    | password= {pwd}
    expected result = {expected_code}
    actual result = {status_code}
    ==>  {test_status}
    '''
    # query status
    status_code = r.status_code
    # display the results
    if status_code == user['expected_code']:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    output = output.format(status_code=status_code,
                           test_status=test_status,
                           expected_code=user['expected_code'],
                           usr=user['username'],
                           pwd=user['password'])
    # printing in a file
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            file.write(output)
    else:
        print(output)

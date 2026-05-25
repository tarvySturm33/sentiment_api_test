import requests


class RequestBuilder:

    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port

    def build_url(self, endpoint):
        return f'http://{self.host}:{self.port}{endpoint}'

    def get(self, endpoint, params=None):
        url = self.build_url(endpoint)
        return requests.get(url=url, params=params)

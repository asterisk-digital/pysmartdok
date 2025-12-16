import json
from array import ArrayType
from typing import List, Dict

import requests


class SmartDokApiError(Exception):
    pass


class ApiClient:
    def __init__(self, api_token: str):
        if api_token is None or api_token == '':
            raise ValueError('api_token must be a valid string')
        self.api_token = api_token
        self.api_url = 'https://api.smartdok.no/'
        self.headers = {}
        self.authenticate()

    def authenticate(self):
        url = self.api_url + 'Authorize/ApiToken'
        post_body = json.dumps({'Token': self.api_token})
        response = requests.post(url, data=post_body, headers={'Content-Type': 'application/json'})
        if response.status_code >= 300:
            raise SmartDokApiError(
                'Failed to authenticate with SmartDok API.'
                + ' Response code: ' + str(response.status_code)
                + ' Response body: ' + response.text)

        # The session token contains quotes, so we need to remove them
        session_token = response.text.replace('"', '')

        self.headers = {'Authorization': 'Bearer ' + session_token}

    def get_qd(self) -> List[Dict]:
        url = self.api_url + 'qd/v2'
        response = requests.get(url, headers=self.headers)
        if response.status_code >= 300:
            raise SmartDokApiError(
                'Failed to get QD data from SmartDok API.'
                + ' Response code: ' + str(response.status_code)
                + ' Response body: ' + response.text)

        if 'Items' not in response.json():
            raise SmartDokApiError('Failed to get QD data from SmartDok API. Items not found in response.'
                                   + ' Response body: ' + response.text)

        items = response.json()['Items']

        return items

    def get_rue(self) -> list[dict]:
        url = self.api_url + "rue"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        if 'Items' not in response.json():
            raise SmartDokApiError('Failed to get QD data from SmartDok API. Items not found in response.'
                                   + ' Response body: ' + response.text)

        items = response.json()['Items']

        return items

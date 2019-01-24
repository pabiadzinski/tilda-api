import json

import requests

from urllib.error import URLError
from urllib.parse import urlencode

from .endpoint import *

ENDPOINT = 'http://api.tildacdn.info/v1/'
STATUS_OK = 'FOUND'
STATUS_ERROR = 'ERROR'

PAGE_ID_PARAM = 'pageid'
PROJECT_ID_PARAM = 'projectid'

STATUS_FIELD = 'status'
RESULT_FIELD = 'result'


class Client(object):

    def __init__(self, secret_key, public_key):
        self.secret_key = secret_key
        self.public_key = public_key

    def _do_request(self, method, params=None):
        payload = {
            'publickey': self.public_key,
            'secretkey': self.secret_key
        }

        if params is not None:
            payload.update(params)

        try:
            url = ENDPOINT + method + '?' + urlencode(payload)
            response = requests.get(url)
        except URLError as e:
            response = e

        json_data = response.content
        data = json.loads(json_data.decode('utf-8'))

        return data.get(RESULT_FIELD)

    def get_project_export(self, project_id):
        return self._do_request(Endpoint.GET_PROJECT_EXPORT, {PROJECT_ID_PARAM: project_id})

    def get_pages_list(self, project_id):
        return self._do_request(Endpoint.GET_PAGES_LIST, {PROJECT_ID_PARAM: project_id})

    def get_page_full_export(self, page_id):
        return self._do_request(Endpoint.GET_PAGE_FULL_EXPORT, {PAGE_ID_PARAM: page_id})

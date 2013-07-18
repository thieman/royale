""" Client for pushing data to Royale. """

import requests

class RoyaleAPI(object):

    def __init__(self, target):
        self.target = target
        if '://' not in target:
            self.target = 'http://' + self.target

    def get(self, endpoint, resource_id=None):
        return self._request_json(requests.get, endpoint, resource_id)

    def post(self, endpoint, resource_id, data):
        return self._request_json(requests.post, endpoint, resource_id, data)

    def put(self, endpoint, resource_id, data):
        return self._request_json(requests.put, endpoint, resource_id, data)

    def delete(self, endpoint, resource_id):
        return self._request_json(requests.delete, endpoint, resource_id)

    def _request_json(self, method, endpoint, resource_id=None, data=None):
        args = [self._join(endpoint, resource_id)]
        kwargs = {}
        if data:
            kwargs['data'] = data
        r = method(*args, **kwargs)
        return r.json() if r.text else {}

    def _join(self, endpoint, resource_id=None):
        parts = [self.target, endpoint]
        if resource_id:
            parts.append(resource_id)
        return '/'.join([s.strip('/') for s in parts])

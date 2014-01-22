import requests
import json

class UwsgiItClient:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

        self.resources = {
            'me': {
                'methods': ['GET', 'POST'],
                'path': 'me',
            },
            'distros': {
                'methods': ['GET'],
                'path': 'distros',
            },
            'containers': {
                'methods': ['GET', 'POST'],
                'path': 'containers',
            },
            'me/containers': {
                'methods': ['GET'],
                'path': 'me/containers',
            },
            'domains': {
                'methods': ['GET', 'POST', 'DELETE'],
                'path': 'domains',
            }
        }

    def _parse_response(self, response):
        try:
            response.raise_for_status()
            response.uerror = False
            response.umessage = ""
        except requests.exceptions.HTTPError as e:
            response.umessage = e.message
            response.uerror = True

        return response

    def _path_join(self, path_list):
        # there should be only integers and strings
        path = []
        for p in path_list:
            if isinstance(p, int):
                path.append("%d" % (p))
            else:
                path.append(p.strip('/'))
        return '/'.join(path)

    def _build_uri(self, path):
        return self._path_join([self.url, path])

    def _get(self, path):
        uri = self._build_uri(path)
        r = requests.get(uri, auth=(self.username, self.password))
        return self._parse_response(r)

    def _post(self, path, data):
        uri = self._build_uri(path)
        payload = json.dumps(data)
        r = requests.post(uri, data=payload, auth=(self.username, self.password))
        return self._parse_response(r)

    def _delete(self, path, data=None):
        uri = self._build_uri(path)
        if data:
            payload = json.dumps(data)
        else:
            payload = None
        r = requests.delete(uri, data=payload, auth=(self.username, self.password))
        return self._parse_response(r)

    def _path_from_resource(self, resource, method):
        resource_is_list = isinstance(resource, list)
        if resource_is_list:
            r = resource[0]
        else:
            r = resource
        res = self.resources.get(r)

        if not res:
            raise ValueError("resource does not exist")

        if method not in res['methods']:
            raise ValueError("method not supported for this resource")

        path = [res['path']]
        if resource_is_list:
            path += resource[1:]

        return self._path_join(path)

    """
    Public API
    """
    # base methods
    def get(self, resource):
        path = self._path_from_resource(resource, 'GET')
        return self._get(path)

    def post(self, resource, data):
        path = self._path_from_resource(resource, 'POST')
        return self._post(path, data)

    def delete(self, resource, data=None):
        path = self._path_from_resource(resource, 'DELETE')
        return self._delete(path, data)

    # wrappers!
    def me(self):
        return self.get("me")

    def containers(self):
        return self.get("me/containers")

    def container(self, id):
        return self.get(["containers", id])

    def distros(self):
        return self.get("distros")

    def domains(self):
        return self.get("domains")

    def update_me(self, data):
        return self.post("me", data)

    def add_domain(self, domain):
        return self.post("domains", {'name': domain })

    def delete_domain(self, domain):
        return self.delete("domains", {'name': domain })

    def update_container(self, container, data):
        return self.post(["containers", container], data)

    def container_set_distro(self, container, distro):
        return self.update_container(container, {'distro': distro })

    def container_set_keys(self, container, keys):
        return self.update_container(container, {'ssh_keys': keys })

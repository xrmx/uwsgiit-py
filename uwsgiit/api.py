import requests
import json

class UwsgiItAlarmLevel:
    SYSTEM    = 0
    USER      = 1
    EXCEPTION = 2
    TRACEBACK = 3
    LOG       = 4

class UwsgiItClient(object):
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def _parse_response(self, response):
        try:
            response.raise_for_status()
            response.uerror = False
            response.umessage = ""
        except requests.exceptions.HTTPError as e:
            response.umessage = str(e)
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
        if isinstance(path, list):
            url = [self.url] + path
        else:
            url = [self.url, path]
        return self._path_join(url)

    def _get(self, path, params=None):
        uri = self._build_uri(path)
        r = requests.get(uri, auth=(self.username, self.password), params=params)
        return self._parse_response(r)

    def _post(self, path, data, params):
        uri = self._build_uri(path)
        payload = json.dumps(data)
        r = requests.post(uri, data=payload, params=params, auth=(self.username, self.password))
        return self._parse_response(r)

    def _delete(self, path, data=None):
        uri = self._build_uri(path)
        if data:
            payload = json.dumps(data)
        else:
            payload = None
        r = requests.delete(uri, data=payload, auth=(self.username, self.password))
        return self._parse_response(r)

    def _check_params(self, params, whitelist):
        if params:
            wrong_params = [p for p in params if p not in whitelist]
            if wrong_params:
                raise KeyError("Invalid params: {0}".format(", ".join(wrong_params)))

    """
    Public API
    """
    # base methods
    def get(self, resource, params=None):
        return self._get(resource, params)

    def post(self, resource, data, params=None):
        return self._post(resource, data, params)

    def delete(self, resource, data=None):
        return self._delete(resource, data)

    # wrappers!
    def news(self):
        return self.get("news")

    def me(self):
        return self.get("me")

    def containers(self, tags=None):
        if tags:
            params = {"tags": ",".join(tags)}
        else:
            params = None
        return self.get("containers", params)

    def container(self, id):
        return self.get(["containers", id])

    def distros(self):
        return self.get("distros")

    def domains(self, tags=None):
        if tags:
            params = {"tags": ",".join(tags)}
        else:
            params = None
        return self.get("domains", params)

    def domain(self, id):
        return self.get(["domains", id])

    def update_me(self, data):
        return self.post("me", data)

    def add_domain(self, domain):
        return self.post("domains", {'name': domain})

    def delete_domain(self, domain):
        return self.delete("domains", {'name': domain})

    def update_domain(self, domain, data):
        return self.post(["domains", domain], data)

    def update_container(self, container, data):
        return self.post(["containers", container], data)

    def container_set_distro(self, container, distro):
        return self.update_container(container, {'distro': distro})

    def container_set_keys(self, container, keys):
        return self.update_container(container, {'ssh_keys': keys})

    def reboot_container(self, container):
        return self.post(["containers", container], {'reboot': 1})

    def create_tag(self, name):
        return self.post("tags", {"name": name})

    def delete_tag(self, tag_id):
        return self.delete(["tags", tag_id])

    def list_tags(self):
        return self.get("tags")

    def container_metric(self, container, metric, params=None):
        return self.get(['metrics', 'container.{}'.format(metric), container], params)

    def domain_metric(self, domain, metric, params=None):
        return self.get(['metrics', 'domain.{}'.format(metric), domain], params)

    def loopboxes(self, container=None, tags=None):
        params = {}
        if tags:
            params['tags'] = ','.join(tags)
        if container:
            params['container'] = container
        return self.get('loopboxes', params)

    def loopbox(self, id):
        return self.get(['loopboxes', id])

    def create_loopbox(self, container, filename, mountpoint, readonly=False):
        return self.post('loopboxes', {'container': container, 'filename': filename, 'mountpoint': mountpoint, 'ro': readonly})

    def update_loopbox(self, id, data):
        return self.post(['loopboxes', id], data)

    def delete_loopbox(self, id):
        return self.delete(['loopboxes', id])

    def alarms(self, params=None):
        ALLOWED_PARAMS = (
            'container', 'class', 'color', 'vassal', 'level',
            'line', 'filename', 'func', 'with_total', 'range'
        )
        self._check_params(params, ALLOWED_PARAMS)
        return self.get('alarms', params)

    def alarm(self, id):
        return self.get(['alarms', id])

    def create_alarm(self, container, message, params=None):
        ALLOWED_PARAMS = (
            'class', 'color', 'vassal', 'level',
            'line', 'filename', 'func', 'unix'
        )
        self._check_params(params, ALLOWED_PARAMS)
        return self.post(['alarms', 'raise', container], message, params)

    def create_alarm_key(self, container):
        return self.get(['alarm_key', container])

    def delete_alarm(self, id):
        return self.delete(['alarms', id])

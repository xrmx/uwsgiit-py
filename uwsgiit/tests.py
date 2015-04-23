import unittest
import os
import random
import uuid

from uwsgiit.api import UwsgiItClient as UClient


class ClientTestCase(unittest.TestCase):
    """
    https://github.com/unbit/uwsgi.it/blob/master/CustomerQuickstart.md
    """

    def setUp(self):
        username = os.environ.get('UWSGI_IT_USERNAME', 'cicciopasticcio')
        password = os.environ.get('UWSGI_IT_PASSWORD', 'cicciopasticcio')
        self.url = os.environ.get('UWSGI_IT_URL', 'http://127.0.0.1:8000/api')
        self.client = UClient(username, password, self.url)

        self.container = os.environ.get('UWSGI_IT_CONTAINER', '30001')
        self.loopbox = os.environ.get('UWSGI_IT_LOOPBOX', '1')
        self.alarm = os.environ.get('UWSGI_IT_ALARM', '1')

    """
    News: curl https://kratos:deimos@foobar.com/api/news/
    """
    def test_news_get(self):
        r = self.client.news()
        news = r.json()
        self.assertEqual(r.uerror, False)

    def test_news_get_without_credentials(self):
        client = UClient(None, None, self.url)
        r = client.news()
        news = r.json()
        self.assertEqual(r.uerror, False)

    """
    Account Info: curl https://kratos:deimos@foobar.com/api/me/
    """

    def test_me_get(self):
        r = self.client.me()
        me = r.json()
        self.assertEqual(r.uerror, False)

    def test_me_post_company(self):
        company = "DogeCom"
        r = self.client.update_me({'company': company})
        self.assertEqual(r.uerror, False)

        r = self.client.me()
        me = r.json()
        self.assertEqual(me['company'], company)

    """
    Distributions: curl https://kratos:deimos17@foobar.com/api/distros/
    """

    def test_distros_get(self):
        r = self.client.distros()
        distros = r.json()
        self.assertEqual(r.uerror, False)

    """
    Containers: curl https://kratos:deimos@foobar.com/api/me/containers/
    """

    def test_containers_get(self):
        r = self.client.containers()
        containers = r.json()
        self.assertEqual(r.uerror, False)

    def test_containers_get_single(self):
        r = self.client.container(self.container)
        container = r.json()
        self.assertEqual(r.uerror, False)

    def test_containers_set_distro(self):
        distros = self.client.distros().json()
        distro = random.choice([d['id'] for d in distros])
        r = self.client.container_set_distro(self.container, distro)
        self.assertEqual(r.uerror, False)

        r = self.client.container(self.container)
        container = r.json()
        self.assertEqual(container['distro'], distro)

    def test_containers_set_keys(self):
        keys = ["ssh-rsa miao"]
        r = self.client.container_set_keys(self.container, keys)
        self.assertEqual(r.uerror, False)

        r = self.client.container(self.container)
        container = r.json()
        self.assertEqual(container['ssh_keys'], keys)

    """
    Domains: curl https://kratos:deimos@foobar.com/api/domains/
    """

    def test_domains_get(self):
        r = self.client.domains()
        domains = r.json()
        self.assertEqual(r.uerror, False)

    def tests_domains_get_single(self):
        r = self.client.domain(100)
        self.assertEqual(r.status_code, 404)

    def test_domains_add_delete(self):
        domain = str(uuid.uuid4())
        # add
        r = self.client.add_domain(domain)
        # lame but fails without settings the dns
        self.assertEqual(r.uerror, True)
        self.assertEqual("FORBIDDEN" in r.umessage, True)

        # delete
        # lame but delete fails if domain does not exist
        self.client.delete_domain(domain)
        self.assertEqual(r.uerror, True)
        self.assertEqual("FORBIDDEN" in r.umessage, True)

        r = self.client.domains()
        domains = r.json()
        found = [d for d in domains if d['name'] == domain]
        self.assertEqual(found, [])

    """
    Tags: curl https://kratos:deimos@foobar.com/api/tags/
    """

    def test_tag_creation_delete(self):
        r = self.client.create_tag("mytag")
        tag_id = r.json()["id"]
        r = self.client.delete_tag(tag_id)
        r = self.client.list_tags()
        tags = r.json()
        found_tag = [t for t in tags if t['id'] == tag_id]
        self.assertEqual(found_tag, [])

    def test_tag_domain_filter(self):
        r = self.client.domains(tags=["ciao"])
        domains = r.json()
        self.assertEqual(r.uerror, False)

    def test_tag_container_filter(self):
        r = self.client.containers(tags=["ciao"])
        containers = r.json()
        self.assertEqual(r.uerror, False)

    """
    Reboot: curl -X POST -d '{"reboot":1}' https://kratos:deimos17@foobar.com/api/containers/30009
    """

    def test_reboot(self):
        r = self.client.reboot_container(self.container)
        self.assertEqual(r.uerror, False)

    """
    Metrics: curl https://kratos:deimos@foobar.com/api/metrics/container.io.read/
             curl https://kratos:deimos@foobar.com/api/metrics/domain.net.rx/
    """

    def test_container_metric(self):
        r = self.client.container_metric(self.container, "io.read")
        self.assertEqual(r.uerror, False)

    def test_domain_metric(self):
        r = self.client.domains()
        domain = r.json()[0]['id']
        r = self.client.domain_metric(domain, "net.rx")
        self.assertEqual(r.uerror, False)

    """
    Loopboxes: curl https://kratos:deimos@foobar.com/api/loopboxes/
    """
    def test_loopboxes(self):
        r = self.client.loopboxes()
        loopboxes = r.json()
        self.assertEqual(r.uerror, False)

    def test_loopboxes_creation_delete(self):
        r = self.client.create_loopbox(self.container, 'myloopbox', 'myloop')
        created_message = r.json()['message']
        self.assertEqual(created_message, 'Created')

        r = self.client.loopboxes()
        loopboxes = r.json()
        loopbox_id = [x['id'] for x in loopboxes if x['container'] == int(self.container) and x['filename'] == 'myloopbox' and x['mountpoint'] == 'myloop'][0]

        r = self.client.delete_loopbox(loopbox_id)
        deleted_message = r.json()['message']
        self.assertEqual(deleted_message, 'Ok')

    def test_loopbox(self):
        r = self.client.loopbox(self.loopbox)
        loopbox = r.json()
        self.assertEqual(r.uerror, False)

    """
    Alarms: curl https://kratos:deimos@foobar.com/api/alarms/
    """
    def test_alarms_get(self):
        r = self.client.alarms()
        alarms = r.json()
        self.assertEqual(r.uerror, False)

    def test_alarms_creation_delete(self):
        params = {
            'class': 'my-uwsgiit-py-testclass'
        }
        r = self.client.create_alarm(self.container, 'myalarm', params)
        created_message = r.json()['message']
        self.assertEqual(created_message, 'Created')

        r = self.client.alarms(params)
        alarms = r.json()
        self.assertEqual(len(alarms), 1)
        alarm_id = alarms[0]['id']

        r = self.client.delete_alarm(alarm_id)
        deleted_message = r.json()['message']
        self.assertEqual(deleted_message, 'Ok')

    def test_alarm(self):
        r = self.client.alarm(self.alarm)
        alarm = r.json()
        self.assertEqual(r.uerror, False)

    def test_alarms_invalid_key(self):
        self.assertRaises(KeyError, self.client.alarms, {'foo': 'bar'})

    def test_create_alarm_key(self):
        r = self.client.create_alarm_key(self.container)
        key = r.json()
        self.assertEqual(r.uerror, False)

    def test_create_alarm_invalid_key(self):
        self.assertRaises(KeyError, self.client.create_alarm, self.container, 'hi there', {'foo': 'bar'})

if __name__ == '__main__':
    unittest.main()

from unittest import TestCase
from uwsgiit.api import UwsgiItClient as UClient
import os, random, uuid

class ClientTestCase(TestCase):
    """
    https://github.com/unbit/uwsgi.it/blob/master/CustomerQuickstart.md
    """
    def setUp(self):
        username = os.environ['UWSGI_IT_USERNAME']
        password = os.environ['UWSGI_IT_PASSWORD']
        url = os.environ['UWSGI_IT_URL']
        self.client = UClient(username, password, url)

        self.container = os.environ['UWSGI_IT_CONTAINER']

    """
    Account Info: curl https://kratos:deimos@foobar.com/api/me/
    """
    def test_me_get(self):
        r = self.client.me()
        me = r.json()
        self.assertEqual(r.uerror, False)

    def test_me_post_company(self):
        company = "DogeCom"
        r = self.client.update_me({'company': company })
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

    # invalid resource
    def test_invalid_resource_get(self):
        self.assertRaises(ValueError, self.client.get, ["doge"])

    def test_invalid_resource_post(self):
        self.assertRaises(ValueError, self.client.post, None, {"resource": "doge", "data": {}})

    def test_invalid_resource_delete(self):
        self.assertRaises(ValueError, self.client.delete, ["doge"])

    # invalid methods
    def test_invalid_post(self):
        self.assertRaises(ValueError, self.client.post, None, {"resource": "distros", "data":{}})

    def test_invalid_delete(self):
        self.assertRaises(ValueError, self.client.delete, ["distros"])

if __name__ == '__main__':
    unittest.main()

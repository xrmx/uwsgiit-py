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

if __name__ == '__main__':
    unittest.main()

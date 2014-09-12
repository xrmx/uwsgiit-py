# uwsgiit-py

A python client library for uwsgi.it.

## Installation

```bash
pip install uwsgiit-py
```

## Usage

To use the API
```python
from uwsgiit.api import UwsgiItClient

client = UwsgiItClient("kratos", "deimos", "https://foobar.com/api")
```

#### Get latest news

```bash
# Plain Usage
curl https://kratos:deimos@foobar.com/api/news/
```

```python
client.news()
```

#### List your data

```bash
# Plain Usage
curl https://kratos:deimos@foobar.com/api/me/
```

```python
client.me()
```

####  Change company name

```bash
# Plain Usage
curl -X POST -d '{"company": "God of War 4 S.p.a."}' https://kratos:deimos@foobar.com/api/me/
```

```python
client.update_me({'company': 'God of War 4 S.p.a.'})
```

#### Change password

```bash
# Plain Usage
curl -X POST -d '{"password": "deimos17"}' https://kratos:deimos@foobar.com/api/me/
```

```python
client.update_me({'password': 'deimos17'})
```

#### List your containers

```bash
# Plain Usage
curl https://kratos:deimos17@foobar.com/api/me/containers/
```

```python
client.containers()
```

#### Show a single container

```bash
# Plain Usage
curl https://kratos:deimos17@foobar.com/api/containers/30009
```

```python
client.container(30009)
```

#### List distros

```bash
# Plain Usage
curl https://kratos:deimos17@foobar.com/api/distros/
```

```python
client.distros()
```

#### Set container distro

```bash
# Plain Usage
curl -X POST -d '{"distro": 2}' https://kratos:deimos17@foobar.com/api/containers/30009
```

```python
client.container_set_distro(30009, 2)
```

#### Upload ssh keys

```bash
# Plain Usage
curl -X POST -d '{"ssh_keys": ["ssh-rsa ........."]}' https://kratos:deimos17@foobar.com/api/containers/30009
```

```python
client.container_set_keys(30009, ["ssh-rsa ........."])
```

#### List domains

```bash
# Plain Usage
curl https://kratos:deimos17@foobar.com/api/domains/
```

```python
client.domains()
```

#### Add domain

```bash
# Plain Usage
curl -X POST -d '{"name":"mynewdomain.org"}' https://kratos:deimos17@foobar.com/api/domains/
```

```python
client.add_domain("mynewdomain.org")
```

#### Delete domain

```bash
# Plain Usage
curl -X DELETE -d '{"name":"mynewdomain.org"}' https://kratos:deimos17@foobar.com/api/domains/
```

```python
client.delete_domain("mynewdomain.org")
```

## Error handling

All the client methods return a [requests'](https://github.com/kennethreitz/requests) Request instance.
To ease error handling the instance is augmentend with two more attributes:
* uerror: a boolean that indicate if an HTTP error occured
* umessage: the error message in plain text

## Acknowledgements

Mikamai's [ruby client](https://github.com/mikamai/uwsgi_it_client/) used as
reference

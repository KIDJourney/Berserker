import requests
from requests.packages.urllib3.util import parse_url


def show_host_info(url):
    response = requests.head(url)
    url_parts = parse_url(url)

    server_software = response.headers.get('server', 'UnKnown')
    server_host = url_parts.host or "Unknown"
    server_port = None
    server_path = url_parts.path or '/'

    if not url_parts.port and url_parts.scheme == 'https':
        server_port = 443
    if not url_parts.port and url_parts.scheme == 'http':
        server_port = 80
    if url_parts.port:
        server_port = url_parts.port

    print("""
Server Software: \t {}
Server Hostname: \t {}
Server Port:     \t {}

Document Path:   \t {}
""".format(server_software, server_host, server_port, server_path))


def show_intro():
    output = """
Berserker
Smoking Test For You Web Application."""
    print(output)


def check_url(url):
    url_part = parse_url(url)
    return url_part.scheme and url_part.netloc

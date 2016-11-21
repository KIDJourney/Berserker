import os
import sys
import json
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


def parse_config_file(file_path):
    """read request config from file"""
    if not os.path.exists(file_path):
        raise Exception("File not exit : {}".format(file_path))

    configs = open(file_path).read()
    try:
        configs = json.loads(configs)
    except Exception as exc:
        raise Exception("Json not valid")

    ret = []

    for index, config in enumerate(configs):
        temp_config = dict()
        temp_config['options'] = {}

        url = config.get('url', '')
        if not check_url(url):
            if url:
                raise Exception("url not valid {}.".format(url))
            else:
                raise Exception('url not exist in {}th config.'.format(index))

        temp_config['url'] = url
        temp_config['concurrency'] = config.get('concurrency', 1)
        temp_config['request_nums'] = config.get('request_nums', 1)
        temp_config['method'] = config.get('method', 'GET')

        temp_config['options']['headers'] = config.get('headers', {})
        temp_config['options']['cookies'] = config.get('cookies', {})

        if config.get('data'):
            temp_config['options']['data'] = config.get('data')

        ret.append(temp_config)

    return ret

import pytest
import unittest
import requests
import time
from urllib import parse as urlparse
from berserker import benchmark
from .web_app import start
from berserker.core import HTTP_VERBS


def _str(item):
    if isinstance(item, dict):
        return '='.join([i for value in item.items() for i in value])
    if isinstance(item, list):
        return '\n'.join([_str(i) for i in item])


class TestBerserker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = start()
        cls.url = 'http://0.0.0.0:23333'
        while True:
            try:
                requests.get(cls.url)
                return
            except requests.ConnectionError:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()

    def setUp(self):
        self.reset()

    def reset(self):
        requests.get(urlparse.urljoin(self.url, 'reset'))

    def get_count(self):
        return int(requests.get(urlparse.urljoin(self.url, 'count')).content)

    def test_request_num(self):
        benchmark(self.url, concurrent=1, request_nums=233)
        result = self.get_count()
        assert result == 233

    def test_with_cookie(self):
        options = {
            'cookies': {'test': 'test'}
        }
        result = benchmark(urlparse.urljoin(self.url, 'cookie'), options=options)
        responses = result.responses
        for response in responses:
            assert _str(options['cookies']) in response.text

    def test_with_header(self):
        options = {
            'headers': {'self_defined_header': 'blablabla'}
        }
        result = benchmark(urlparse.urljoin(self.url, 'header'), options=options)
        responses = result.responses
        for response in responses:
            assert 'HTTP_{}={}'.format('self_defined_header'.upper(), 'blablabla') in response.text

    def test_request_method(self):
        for method in HTTP_VERBS:
            result = benchmark(urlparse.urlparse(self.url, 'method'), method=method)
            responses = result.responses
            for response in responses:
                assert method in response.text

    def test_connect_error(self):
        result = benchmark('http://127.0.0.1:23232', request_nums=5, concurrent=1)
        assert len(result.errors) == 5

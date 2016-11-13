import unittest
import requests
import time
from urllib import parse as urlparse
from berserker import benchmark
from .web_app import start


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

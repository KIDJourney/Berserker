import pytest
import unittest
from unittest import mock
from berserker.helper import parse_config_file


class TestHelper(unittest.TestCase):
    @mock.patch('builtins.open')
    @mock.patch('berserker.helper.os.path.exists')
    def test_basic_parse_json_config(self, mock_os, mock_open):
        mock_open.return_value.read.return_value = """[{"method": "post", "cookies": {"ca": "cv", "cb": "cv2"}, "data": {"key2": "value2", "key": "value"}, "url": "http://example.com", "headers": {"name2": "value2", "name": "value"}, "request_nums": 1000, "concurrency": 100}]"""
        mock_os.return_value = True
        parser_result = parse_config_file('est')

        assert parser_result == [
            {
                "concurrency": 100,
                "request_nums": 1000,
                'url': 'http://example.com',
                'method': 'post',
                'options': {
                    'cookies': {'ca': 'cv', 'cb': 'cv2'},
                    'headers': {
                        'name': 'value',
                        'name2': 'value2'
                    },
                    'data': {
                        'key': 'value',
                        'key2': 'value2'
                    }
                }
            }
        ]

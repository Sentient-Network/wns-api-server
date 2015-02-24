__author__ = 'mdavid'

# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

from unittest import TestCase

from mock import patch, Mock

import netki.api.util

class Test_create_json_response(TestCase):

    def setUp(self):

        self.patcher1 = patch('netki.api.util.request')
        self.patcher2 = patch('netki.api.util.current_app')
        self.patcher3 = patch('netki.api.util.Response')

        self.mockRequest = self.patcher1.start()
        self.mockCurrentApp = self.patcher2.start()
        self.mockResponse = self.patcher3.start()

        # Setup Referrer
        self.mockRequest.referrer = 'http://127.0.0.1'
        self.mockRequest.url_rule.rule = '/mockrule'

        # Setup App
        rule_obj = Mock()
        rule_obj.rule = '/mockrule'
        rule_obj.methods = ['POST', 'PUT', 'OPTIONS']

        app_obj = Mock()
        app_obj.url_map = Mock()
        app_obj.url_map._rules = [rule_obj]

        self.mockCurrentApp._get_current_object.return_value = app_obj

    def tearDown(self):

        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def test_goright(self):

        # Run create_json_response
        ret_val = netki.api.util.create_json_response(success=True, message='test message', data={'key':'value'})

        # Verify Response Data
        respdata = self.mockResponse.call_args[0]
        self.assertEqual(respdata[0], '{"message": "test message", "key": "value", "success": true}')

        # Verify Response Arguments
        respargs = self.mockResponse.call_args[1]
        self.assertEqual(respargs['status'], 200)
        self.assertEqual(respargs['mimetype'], 'application/json')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Headers'], 'X-Requested-With, accept, content-type')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Methods'], 'PUT, POST, OPTIONS')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Origin'], 'http://127.0.0.1')

    def test_no_matching_methods(self):

        # Setup Testcase
        self.mockCurrentApp._get_current_object.return_value.url_map._rules = []

        # Run create_json_response
        ret_val = netki.api.util.create_json_response(success=True, message='test message', data={'key':'value'})

        # Verify Response Data
        respdata = self.mockResponse.call_args[0]
        self.assertEqual(respdata[0], '{"message": "test message", "key": "value", "success": true}')

        # Verify Response Arguments
        respargs = self.mockResponse.call_args[1]
        self.assertEqual(respargs['status'], 200)
        self.assertEqual(respargs['mimetype'], 'application/json')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Headers'], 'X-Requested-With, accept, content-type')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Methods'], '')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Origin'], 'http://127.0.0.1')

    def test_open_origin_for_now_TODO(self):

        # Setup Testcase
        self.mockRequest.referrer = 'http://google.com'

        # Run create_json_response
        ret_val = netki.api.util.create_json_response(success=True, message='test message', data={'key':'value'})

        # Verify Response Data
        respdata = self.mockResponse.call_args[0]
        self.assertEqual(respdata[0], '{"message": "test message", "key": "value", "success": true}')

        # Verify Response Arguments
        respargs = self.mockResponse.call_args[1]
        self.assertEqual(respargs['status'], 200)
        self.assertEqual(respargs['mimetype'], 'application/json')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Headers'], 'X-Requested-With, accept, content-type')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Methods'], 'PUT, POST, OPTIONS')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Origin'], '*')

    def test_message_message_success_override(self):

        # Run create_json_response
        ret_val = netki.api.util.create_json_response(success=True, message='test message', data={'message':'value', 'success': False, 'key': 'value'})

        # Verify Response Data
        respdata = self.mockResponse.call_args[0]
        self.assertEqual(respdata[0], '{"message": "test message", "key": "value", "success": true}')

        # Verify Response Arguments
        respargs = self.mockResponse.call_args[1]
        self.assertEqual(respargs['status'], 200)
        self.assertEqual(respargs['mimetype'], 'application/json')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Headers'], 'X-Requested-With, accept, content-type')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Methods'], 'PUT, POST, OPTIONS')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Origin'], 'http://127.0.0.1')

    def test_status_204(self):

        # Run create_json_response
        ret_val = netki.api.util.create_json_response(success=True, message='test message', data={'key':'value'}, status=204)

        # Verify Response Data
        respdata = self.mockResponse.call_args[0]
        self.assertIsNone(respdata[0])

        # Verify Response Arguments
        respargs = self.mockResponse.call_args[1]
        self.assertEqual(respargs['status'], 204)
        self.assertEqual(respargs['mimetype'], 'application/json')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Headers'], 'X-Requested-With, accept, content-type')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Methods'], 'PUT, POST, OPTIONS')
        self.assertEqual(respargs['headers']['Access-Control-Allow-Origin'], 'http://127.0.0.1')

if __name__ == "__main__":
    import unittest
    unittest.main()
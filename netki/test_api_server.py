__author__ = 'mdavid'

# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

from unittest import TestCase

import netki.api_server

class Test_utility_functions(TestCase):

    def test_index_status_route(self):

        ret_val = netki.api_server.index()
        self.assertEqual(200, ret_val.status_code)
        self.assertEqual('UP', ret_val.data)
        self.assertEqual('text/html', ret_val.mimetype)

if __name__ == "__main__":
    import unittest
    unittest.main()
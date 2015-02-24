__author__ = 'frank'

# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

from unittest import TestCase

from mock import patch
import netki.util.logutil


class TestSetupLogging(TestCase):
    def setUp(self):
        self.patcher1 = patch('netki.util.logutil.LogUtil.loggers')
        self.patcher2 = patch('netki.util.logutil.os')
        self.patcher3 = patch('netki.util.logutil.logging')

        self.mockLoggers = self.patcher1.start()
        self.mockOS = self.patcher2.start()
        self.mockLogging = self.patcher3.start()

    def tearDown(self):

        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def test_app_name_exists(self):

        netki.util.logutil.LogUtil.setup_logging(app_name='my_test_app')

        self.assertEqual(self.mockLoggers.get.call_count, 2)
        self.assertFalse(self.mockOS.path.exists.called)
        self.assertEqual(self.mockLoggers.get.call_args_list[1][0][0], 'my_test_app')

    def test_log_path_exists(self):
        self.mockLoggers.get.return_value = None
        self.mockOS.path.exists.return_value = True

        netki.util.logutil.LogUtil.setup_logging()

        self.assertEqual(self.mockLoggers.get.call_count, 1)
        self.assertTrue(self.mockOS.path.exists.called)
        self.assertFalse(self.mockOS.mkdir.called)
        self.assertEqual(self.mockOS.path.abspath.call_args_list[0][0][0], '/var/log')

    def test_log_path_does_not_exist(self):
        self.mockLoggers.get.return_value = None
        self.mockOS.path.exists.return_value = False

        netki.util.logutil.LogUtil.setup_logging()

        self.assertEqual(self.mockLoggers.get.call_count, 1)
        self.assertTrue(self.mockOS.path.exists.called)
        self.assertTrue(self.mockOS.mkdir.called)
        self.assertEqual(self.mockOS.path.abspath.call_args_list[0][0][0], '/var/log')

    def test_log_to_file_false(self):
        self.mockLoggers.get.return_value = None

        netki.util.logutil.LogUtil.setup_logging(log_to_file=False)

        self.assertEqual(self.mockLogging.StreamHandler.call_args_list[0][0][0].name, '<stdout>')
        self.assertTrue('handlers' not in dir(self.mockLogging))

    def test_log_to_file_true(self):
        self.mockLoggers.get.return_value = None
        netki.util.logutil.LogUtil.setup_logging(log_to_file=True)

        self.assertEqual(self.mockLogging.StreamHandler.call_args_list[0][0][0].name, '<stdout>')
        self.assertEqual(self.mockLogging.handlers.TimedRotatingFileHandler.call_args_list[0][0][0], '/var/log/app.log')

if __name__ == "__main__":
    import unittest
    unittest.main()
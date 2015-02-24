__author__ = 'mdavid'

# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

from unittest import TestCase

from mock import patch
from StringIO import StringIO

from netki.common.config import ConfigManager

class ConfigManagerTestCase(TestCase):
    def tearDown(self):
        super(ConfigManagerTestCase, self).tearDown()
        ConfigManager._instances.clear()

class TestConfigManagerInit(ConfigManagerTestCase):

    def setUp(self):

        ConfigManager._instances.clear()

        self.patcher1 = patch('netki.common.config.os.listdir')
        self.patcher2 = patch('netki.common.config.os.path.isfile')
        self.patcher3 = patch('netki.common.config.open', create=True)
        self.patcher4 = patch('netki.common.config.ConfigManager.find_config_file')

        self.mockListdir = self.patcher1.start()
        self.mockIsFile = self.patcher2.start()
        self.mockOpen = self.patcher3.start()
        self.mockFindConfigFile = self.patcher4.start()

        self.mockListdir.side_effect = (['etc'], ['app.test.config'])
        self.mockIsFile.return_value = True

        def empty_func(*args):
            pass

        def return_file_data():
            return StringIO('''
[section]
string_value=string
int_value=1
float_value=42.42
bool_true=true
bool_false=false
        ''')

        mockFile = StringIO()
        mockFile.__enter__ = return_file_data
        mockFile.__exit__ = empty_func
        self.mockOpen.return_value = mockFile

        self.mockFindConfigFile.return_value = 'CONFIGFILE'

    def tearDown(self):

        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()

    def test_init_go_right(self):

        ret_val = ConfigManager()

        self.assertIsNotNone(ret_val)
        self.assertEqual('string', ret_val.config_dict.section.string_value)
        self.assertEqual(1, ret_val.config_dict.section.int_value)
        self.assertEqual(42.42, ret_val.config_dict.section.float_value)
        self.assertTrue(ret_val.config_dict.section.bool_true)
        self.assertFalse(ret_val.config_dict.section.bool_false)

        self.assertEqual(ret_val.config_dict, ret_val.get_config())

        self.assertEqual(1, self.mockFindConfigFile.call_count)
        self.assertEqual(1, self.mockIsFile.call_count)
        self.assertEqual(1, self.mockOpen.call_count)

    def test_no_config_file(self):

        self.mockIsFile.return_value = False

        try:
            ConfigManager()
            self.assertTrue(False)
        except Exception as e:
            self.assertIsNotNone(e)

        self.assertEqual(1, self.mockFindConfigFile.call_count)
        self.assertEqual(1, self.mockIsFile.call_count)
        self.assertEqual(0, self.mockOpen.call_count)

class TestGetConfigFile(ConfigManagerTestCase):

    def setUp(self):

        ConfigManager._instances.clear()
        self.patcher1 = patch('netki.common.config.os.listdir')
        self.mockListDir = self.patcher1.start()
        self.mockListDir.side_effect = ( ['etc'], ['app.test.config'])

    def test_go_right(self):

        ret_val = ConfigManager.find_config_file('test')

        self.assertEqual('./etc/app.test.config', ret_val)
        self.assertEqual(2, self.mockListDir.call_count)

    def test_go_right_no_etc_but_file(self):

        self.mockListDir.side_effect = None
        self.mockListDir.return_value = ['app.test.config']

        ret_val = ConfigManager.find_config_file('test')
        self.assertEqual('./app.test.config', ret_val)

    def test_not_found(self):

        self.mockListDir.side_effect = None
        self.mockListDir.return_value = []

        ret_val = ConfigManager.find_config_file('test')
        self.assertIsNone(ret_val)

if __name__ == "__main__":
    import unittest
    unittest.main()
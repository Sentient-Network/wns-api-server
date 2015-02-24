# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

import string
from unittest import TestCase

from netki.util.validation import InputValidation

__author__ = 'mdavid'


class TestInputValidation(TestCase):

    def test_is_valid_domain(self):

        # Test Empties
        self.assertFalse(InputValidation.is_valid_domain(None))
        self.assertFalse(InputValidation.is_valid_domain(''))

        # Test Valid Domains
        self.assertTrue(InputValidation.is_valid_domain('testdomain.com'))
        self.assertTrue(InputValidation.is_valid_domain('test-domain.com'))
        self.assertTrue(InputValidation.is_valid_domain('72testdomain.com'))
        self.assertTrue(InputValidation.is_valid_domain('subdomain.testdomain.com'))

        # Test Invalid Domains
        self.assertFalse(InputValidation.is_valid_domain('testdomaincom'))
        self.assertFalse(InputValidation.is_valid_domain('test_domain.com'))
        self.assertFalse(InputValidation.is_valid_domain('testdomain!com'))

    def test_is_valid_wallet_name(self):

        # Test Empties
        self.assertFalse(InputValidation.is_valid_wallet_name(None))
        self.assertFalse(InputValidation.is_valid_wallet_name(''))

        # Test Valid Wallet Names
        self.assertTrue(InputValidation.is_valid_wallet_name('walletname'))
        self.assertTrue(InputValidation.is_valid_wallet_name('wallet-name'))
        self.assertTrue(InputValidation.is_valid_wallet_name('72walletname'))

        # Test Invalid Wallet Names
        self.assertFalse(InputValidation.is_valid_wallet_name('wallet.name'))
        self.assertFalse(InputValidation.is_valid_wallet_name('wallet_name'))
        self.assertFalse(InputValidation.is_valid_wallet_name('wallet_name.com'))
        self.assertFalse(InputValidation.is_valid_wallet_name('walletname!com'))


    def test_is_valid_field(self):

        # Test Empties
        self.assertFalse(InputValidation.is_valid_field(None))
        self.assertFalse(InputValidation.is_valid_field(''))

        # Valid Fields
        self.assertTrue(InputValidation.is_valid_field('billybob'))
        self.assertTrue(InputValidation.is_valid_field('billybo-.#(!b75'))

        # Invalid Fields
        self.assertFalse(InputValidation.is_valid_field('[45]vfgdf\\/'))
        self.assertFalse(InputValidation.is_valid_field('();'))
        self.assertFalse(InputValidation.is_valid_field('this@me.com$'))
        self.assertFalse(InputValidation.is_valid_field('`~>'))

    def test_is_valid_wallet_address(self):

        self.assertFalse(InputValidation.is_valid_wallet_address(None))
        self.assertFalse(InputValidation.is_valid_wallet_address(''))

        self.assertTrue(InputValidation.is_valid_wallet_address('kjh4kjh534lkj5h34lkj5h43kj35h'))
        self.assertFalse(InputValidation.is_valid_wallet_address('#@^*^&(&$%'))

    def test_is_valid_currency(self):

        self.assertFalse(InputValidation.is_valid_currency(None))
        self.assertFalse(InputValidation.is_valid_currency(''))

        self.assertTrue(InputValidation.is_valid_currency('btc'))
        self.assertTrue(InputValidation.is_valid_currency('ltc'))
        self.assertTrue(InputValidation.is_valid_currency('dgc'))

        self.assertFalse(InputValidation.is_valid_currency('nmc'))
        self.assertFalse(InputValidation.is_valid_currency('75x12'))

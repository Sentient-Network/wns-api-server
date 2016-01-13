__author__ = 'frank'

# Setup our test environment
import os
os.environ['NETKI_ENV'] = 'test'

from unittest import TestCase

from netki.api.domain import *

from mock import patch, Mock


class TestWalletLookup(TestCase):
    # This is the open wallet name lookup API

    def setUp(self):
        self.patcher1 = patch("netki.api.domain.InputValidation")
        self.patcher2 = patch("netki.api.domain.create_json_response")
        self.patcher3 = patch("netki.api.domain.WalletNameResolver")
        self.patcher4 = patch("netki.api.domain.requests")

        self.mockInputValidation = self.patcher1.start()
        self.mockCreateJSONResponse = self.patcher2.start()
        self.mockWalletNameResolver = self.patcher3.start()
        self.mockRequests = self.patcher4.start()

        config.namecoin.enabled = True
        self.mockRequests.get.return_value.json.return_value = {'success': True, 'wallet_address': '1walletaddy'}

    def tearDown(self):

        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def get_json_call(self):
        # Utility function to get JSON call_args_list cleaning up assertions in below tests
        return self.mockCreateJSONResponse.call_args_list[0][1].get('data')

    def test_invalid_wallet_name_field(self):
        # Used to simulate failure in validation for each iteration [iteration 1, iteration 2, etc.]
        self.mockInputValidation.is_valid_field.side_effect = [False]

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertFalse(self.mockWalletNameResolver.called)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Invalid Parameters')

    def test_invalid_currency_field(self):
        # Used to simulate failure in validation for each iteration [iteration 1, iteration 2, etc.]
        self.mockInputValidation.is_valid_field.side_effect = [True, False]

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertFalse(self.mockWalletNameResolver.called)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Invalid Parameters')

    def test_invalid_wallet_name_field_no_dot(self):

        api_wallet_lookup('walletfrankcontrerasme', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertFalse(self.mockWalletNameResolver.called)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Invalid Parameters')

    def test_wallet_address_returned_success(self):

        self.mockWalletNameResolver.return_value.resolve_wallet_name.return_value = '1djskfaklasdjflkasdf'

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockWalletNameResolver.return_value.set_namecoin_options.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertTrue(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), '')

        # Returned Data Validation
        call_dict = self.get_json_call()
        self.assertEqual(call_dict.get('wallet_name'), 'wallet.frankcontreras.me')
        self.assertEqual(call_dict.get('currency'), 'btc')
        self.assertEqual(call_dict.get('wallet_address'), '1djskfaklasdjflkasdf')

    def test_namecoin_config_disabled(self):

        self.mockWalletNameResolver.return_value.resolve_wallet_name.return_value = '1djskfaklasdjflkasdf'
        config.namecoin.enabled = False

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockWalletNameResolver.return_value.set_namecoin_options.call_count, 0)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertTrue(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), '')

        # Returned Data Validation
        call_dict = self.get_json_call()
        self.assertEqual(call_dict.get('wallet_name'), 'wallet.frankcontreras.me')
        self.assertEqual(call_dict.get('currency'), 'btc')
        self.assertEqual(call_dict.get('wallet_address'), '1djskfaklasdjflkasdf')

    def test_namecoin_use_api_returned_success(self):

        config.namecoin.use_api = True
        config.general.lookup_api_url = 'http://domain.com/lookup'
        self.mockWalletNameResolver.return_value.resolve_wallet_name.return_value = '1djskfaklasdjflkasdf'

        api_wallet_lookup('wallet.frankcontreras.bit', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 1)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.set_namecoin_options.call_count, 0)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertTrue(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), '')

        # Returned Data Validation
        call_dict = self.get_json_call()
        self.assertEqual(call_dict.get('wallet_name'), 'wallet.frankcontreras.bit')
        self.assertEqual(call_dict.get('currency'), 'btc')
        self.assertEqual(call_dict.get('wallet_address'), '1walletaddy')

    def test_namecoin_use_api_returned_failure(self):

        config.namecoin.use_api = True
        config.general.lookup_api_url = 'http://domain.com/lookup'
        self.mockWalletNameResolver.return_value.resolve_wallet_name.return_value = '1djskfaklasdjflkasdf'
        self.mockRequests.get.return_value.json.return_value['success'] = False

        api_wallet_lookup('wallet.frankcontreras.bit', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 1)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.set_namecoin_options.call_count, 0)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)

        # Returned Data Validation
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Wallet Name does not exist')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_insecure_error(self):
        self.mockInputValidation.is_valid_field.return_value = True
        self.mockWalletNameResolver.return_value.resolve_wallet_name.side_effect = WalletNameLookupInsecureError()

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Wallet Name Lookup is Insecure')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_does_not_exist(self):
        self.mockInputValidation.is_valid_field.return_value = True
        self.mockWalletNameResolver.return_value.resolve_wallet_name.side_effect = WalletNameLookupError()

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Wallet Name does not exist')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_empty_currency_list(self):
        self.mockInputValidation.is_valid_field.return_value = True
        self.mockWalletNameResolver.return_value.resolve_wallet_name.side_effect = WalletNameUnavailableError()

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Wallet Name does not exist')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_currency_unavailable(self):
        self.mockInputValidation.is_valid_field.return_value = True
        self.mockWalletNameResolver.return_value.resolve_wallet_name.side_effect = WalletNameCurrencyUnavailableError()

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Wallet Name Does Not Contain Requested Currency')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_exception(self):

        self.mockWalletNameResolver.return_value.resolve_wallet_name.side_effect = Exception('Raising Exception for testing')

        api_wallet_lookup('wallet.frankcontreras.me', 'btc')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 2)
        self.assertEqual(self.mockRequests.get.call_count, 0)
        self.assertEqual(self.mockWalletNameResolver.return_value.resolve_wallet_name.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'General Wallet Lookup Failure')

    def test_uppercase_currency_and_wallet_name_to_lowercase(self):

        api_wallet_lookup('Wallet.FrankContreras.Me', 'BTC')

        # Validate call to resolve has values in lowercase
        call_args = self.mockWalletNameResolver.return_value.resolve_wallet_name.call_args_list[0][0]
        self.assertEqual('wallet.frankcontreras.me', call_args[0])
        self.assertEqual('btc', call_args[1])

    def test_dogecoin_transform(self):

        api_wallet_lookup('wallet.frankContreras.me', 'doge')

        # Validate call to resolve has values in lowercase
        call_args = self.mockWalletNameResolver.return_value.resolve_wallet_name.call_args_list[0][0]
        self.assertEqual('wallet.frankcontreras.me', call_args[0])
        self.assertEqual('dgc', call_args[1])

class TestWalletnameCurrencyLookup(TestCase):

    def setUp(self):
        self.patcher1 = patch("netki.api.domain.InputValidation")
        self.patcher2 = patch("netki.api.domain.create_json_response")
        self.patcher4 = patch("netki.api.domain.WalletNameResolver")

        self.mockInputValidation = self.patcher1.start()
        self.mockCreateJSONResponse = self.patcher2.start()
        self.mockWalletNameResolver = self.patcher4.start()

        self.mockWalletNameResolver.return_value.resolve_available_currencies.return_value = ['btc','ltc']

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher4.stop()

    def get_json_call(self):
        # Utility function to get JSON call_args_list cleaning up assertions in below tests
        return self.mockCreateJSONResponse.call_args_list[0][1].get('data')

    def test_invalid_wallet_name_field(self):
        # Used to simulate failure in validation for each iteration [iteration 1, iteration 2, etc.]
        self.mockInputValidation.is_valid_field.side_effect = [False]

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Invalid Parameters')
        self.assertFalse(self.mockWalletNameResolver.called)

    def test_invalid_wallet_name_field_no_dot(self):

        walletname_currency_lookup('walletfrankcontrerasme')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'Invalid Parameters')
        self.assertFalse(self.mockWalletNameResolver.called)

    def test_wallet_address_returned_success(self):

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertTrue(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), '')
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        # Returned Data Validation
        call_dict = self.get_json_call()
        self.assertEqual(call_dict.get('wallet_name'), 'wallet.frankcontreras.me')
        self.assertEqual(call_dict.get('available_currencies'), ['btc','ltc'])

    def test_wallet_lookup_returned_error(self):

        self.mockInputValidation.is_valid_field.return_value = True

        self.mockWalletNameResolver.return_value.resolve_available_currencies.side_effect = WalletNameUnavailableError()

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'),'Wallet Name Does Not Exist')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_insecure(self):

        self.mockInputValidation.is_valid_field.return_value = True

        self.mockWalletNameResolver.return_value.resolve_available_currencies.side_effect = WalletNameLookupInsecureError()

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'),'Wallet Name Lookup is Insecure')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_currency_unavailable(self):

        self.mockInputValidation.is_valid_field.return_value = True

        self.mockWalletNameResolver.return_value.resolve_available_currencies.side_effect = WalletNameCurrencyUnavailableError()

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'),'Requested Currency Unavailable')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})

    def test_wallet_lookup_returned_currency_namecoin_unavailable(self):

        self.mockInputValidation.is_valid_field.return_value = True

        self.mockWalletNameResolver.return_value.resolve_available_currencies.side_effect = WalletNameNamecoinUnavailable()

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'),'Namecoin-based Wallet Name Lookup Unavailable')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data'), {})


    def test_wallet_lookup_failed(self):
        self.mockInputValidation.is_valid_field.return_value = True
        self.mockWalletNameResolver.return_value.resolve_available_currencies.return_value = None

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'LOOKUP_FAILURE')
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('data').get('wallet_name'), 'wallet.frankcontreras.me')

    def test_wallet_lookup_exception(self):
        self.mockWalletNameResolver.return_value.resolve_available_currencies.side_effect = Exception()

        walletname_currency_lookup('wallet.frankcontreras.me')

        self.assertEqual(self.mockInputValidation.is_valid_field.call_count, 1)
        self.assertEqual(1, self.mockWalletNameResolver.return_value.resolve_available_currencies.call_count)
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])

        self.assertEqual(self.mockCreateJSONResponse.call_count, 1)
        self.assertFalse(self.mockCreateJSONResponse.call_args_list[0][1].get('success'))
        self.assertEqual(self.mockCreateJSONResponse.call_args_list[0][1].get('message'), 'General Wallet Lookup Failure')

    def test_uppercase_currency_and_wallet_name_to_lowercase(self):

        walletname_currency_lookup('wallet.frankcontreras.me')

        # Validate call to resolve has values in lowercase
        self.assertEqual('wallet.frankcontreras.me', self.mockWalletNameResolver.return_value.resolve_available_currencies.call_args[0][0])


if __name__ == "__main__":
    import unittest
    unittest.main()
__author__ = 'mdavid'

import string
import re


class InputValidation:
    @staticmethod
    def is_valid_domain(text):
        if not text:
            return False

        if '.' not in text:
            return False

        allowed = set(string.ascii_letters + string.digits + '-.')
        if set(text) - allowed:
            return False
        return True

    @staticmethod
    def is_valid_wallet_name(text):
        if not text:
            return False

        allowed = set(string.ascii_letters + string.digits + '-')
        if set(text) - allowed:
            return False
        return True

    @staticmethod
    def is_valid_field(text):

        if isinstance(text, float) or isinstance(text, int):
            text = str(text)

        if not text:
            return False

        allowed = set(string.ascii_letters + string.digits + ' -.#,()+!@_')
        if set(text) - allowed:
            return False
        return True

    @staticmethod
    def is_valid_wallet_address(wallet_address):
        if not wallet_address:
            return False

        allowed = set(string.ascii_letters + string.digits)
        if set(wallet_address) - allowed:
            return False
        return True

    @staticmethod
    def is_valid_currency(currency):
        if not currency:
            return False

        return currency in ['btc', 'ltc', 'dgc']


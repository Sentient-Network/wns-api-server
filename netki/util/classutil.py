__author__ = 'mdavid'

# Borrowed from https://wiki.python.org/moin/PythonDecoratorLibrary#Singleton

import functools

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
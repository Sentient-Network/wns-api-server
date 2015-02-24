__author__ = 'mdavid'

import ConfigParser
import os

from attrdict import AttrDict

from netki.util.logutil import LogUtil
from netki.util.classutil import Singleton


log = LogUtil.setup_logging('config_manager')

MAX_CONFIG_DEPTH = 5

class ConfigManager:

    __metaclass__ = Singleton

    def __init__(self, env='prod'):

        self.env = os.environ.get('NETKI_ENV', env)

        config_file = ConfigManager.find_config_file(self.env)

        if not config_file or not os.path.isfile(config_file):
            raise Exception('Cannot Find Config File app.%s.config' % self.env)

        log.info('Loading Configuration [ENV: %s | FILE: %s]' % (self.env, config_file))

        with open(config_file,'r') as file:
            config = ConfigParser.ConfigParser()
            config.readfp(file)

            pre_transform_dict = AttrDict(config._sections)
            for k,v in pre_transform_dict.iteritems():
                if isinstance(v, dict):
                    is_changed = False
                    for key,value in v.items():

                        # Convert Bools
                        if value.strip().lower() == 'true':
                            v[key] = True
                            is_changed = True
                            continue

                        if value.strip().lower() == 'false':
                            v[key] = False
                            is_changed = True
                            continue

                        # Convert Floats
                        try:
                            if '.' in value:
                                v[key] = float(value)
                                is_changed = True
                                continue
                        except ValueError:
                            pass

                        # Convert Ints
                        try:
                            v[key] = int(value)
                            is_changed = True
                            continue
                        except ValueError:
                            pass

                    if is_changed:
                        pre_transform_dict.__setattr__(k,v)

            self.config_dict = pre_transform_dict

    def get_config(self):
        return self.config_dict

    @staticmethod
    def find_config_file(env):

        search_path = '.'
        for i in range(MAX_CONFIG_DEPTH):
            files = [f for f in os.listdir(search_path) if f == 'app.%s.config' % env or f == 'etc']
            if not files:
                search_path = '../%s' % search_path
                continue

            if 'etc' in files:
                etc_files = [f for f in os.listdir('%s/etc' % search_path) if f == 'app.%s.config' % env]
                if etc_files:
                    return '%s/etc/%s' % (search_path, etc_files[0])

            if 'app.%s.config' % env in files:
                return '%s/%s' % (search_path, files[files.index('app.%s.config' % env)])

        return None

if __name__ == '__main__':

    print ConfigManager().get_config()
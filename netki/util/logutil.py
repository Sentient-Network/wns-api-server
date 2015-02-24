__author__ = 'mdavid'

import logging
import logging.handlers
import os
import sys

class LogUtil:

    loggers = {}

    @classmethod
    def setup_logging(cls, app_name='app', log_to_file=False):

        if LogUtil.loggers.get(app_name):
            return cls.loggers.get(app_name)

        logdir = os.path.abspath('/var/log')
        if not os.path.exists(logdir):
            os.mkdir(logdir)

        log = logging.getLogger(app_name)
        log.setLevel(logging.DEBUG)
        log_formatter = logging.Formatter("%(asctime)s [%(process)d] [%(levelname)s] %(funcName)s :: %(message)s")

        if log_to_file:
            fh = logging.handlers.TimedRotatingFileHandler('/var/log/%s.log' % app_name, when="d", interval=1, backupCount=10)
            fh.setFormatter(log_formatter)
            log.addHandler(fh)

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(log_formatter)
        log.addHandler(ch)
        log.info("Logger Initialized [%s]" % app_name)
        cls.loggers[app_name] = log
        return log

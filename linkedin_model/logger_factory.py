__author__ = 'yoav'

import logging
import logging.config

#todo: try to move the config initialization to __initiii.py and get rid of this file
logging.config.fileConfig(r'/Users/yoav/Documents/Git/yoav-sadeh/my-linkedin-connections/linkedin_model/logger.conf')

def get_logger(cls):
    return logging.getLogger(str(type(cls).__name__))


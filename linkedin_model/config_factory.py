__author__ = 'yoav'

from ConfigParser import ConfigParser
import os

def get_config():
    dir = os.path.dirname(__file__)
    absolut_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'dev.conf')
    config = ConfigParser()
    config.read([absolut_path])
    return config

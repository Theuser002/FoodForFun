import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CORE_DATA_DIR = '{}/{}'.format(basedir, 'core_data')
    HOST = 'localhost'
    PORT = 8080
    CLIENT_MAX_SIZE = 40 * 1024 ** 2


class FoodForFunConfig:
    CORE_DATA_DIR = '{}/{}/{}'.format(basedir, 'foodforfun', 'core_data')
    MODEL_VERSION = 1



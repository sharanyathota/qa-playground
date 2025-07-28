import configparser
import os

config = configparser.RawConfigParser()
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configurations', 'config.ini'))
config.read(config_path)
print(f"Reading config file: {config_path}")
print(f"Sections found: {config.sections()}")


class ReadConfig:
    @staticmethod
    def getApplicationURL():
        url = config.get('common_info' , 'base_url')
        return url

    @staticmethod
    def getUserEmail():
        username = config.get('common_info', 'username')
        return username

    @staticmethod
    def getUserPassword():
        password = config.get('common_info', 'password')
        return password

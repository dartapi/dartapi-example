import os
from os.path import join, dirname

from dotenv import load_dotenv


class Config(object):
	def __init__(self, context=".env"):
		load_dotenv(join(dirname(__file__), context))

	@staticmethod
	def get_env_value(key):
		return str(os.environ.get(key))


if __name__ == "__main__":
	config = Config()
	DARTAPI_HOST = config.get_env_value("DARTAPI_HOST")
	print(DARTAPI_HOST)

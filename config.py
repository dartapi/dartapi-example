import os
from os.path import join, dirname

from dotenv import load_dotenv


class Config(object):
	def __init__(self):
		self.load_env(".env")

	@staticmethod
	def get_env_value(key):
		return str(os.environ.get(key))

	@staticmethod
	def load_env(context):
		env = join(dirname(__file__), context)
		load_dotenv(env)


if __name__ == "__main__":
	config = Config()
	DARTAPI_HOST = config.get_env_value("DARTAPI_HOST")
	print(DARTAPI_HOST)

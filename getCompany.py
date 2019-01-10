from config import Config
from dartApiBase import DartApiBase


class GetCompany(DartApiBase):
	def __init__(self, local_config):
		super().__init__(local_config)
		self.config = local_config

	def run(self):
		company = self.get_company("000020")
		print(company)


if __name__ == "__main__":
	config = Config()
	with GetCompany(config) as runner:
		runner.run()

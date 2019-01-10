from config import Config
from dartApiBase import DartApiBase


class ExampleDartApi(DartApiBase):
	def __init__(self, local_config):
		super().__init__(local_config)
		self.config = local_config

	def test_get_company(self):
		company = self.get_company("000020")
		print(company)

	def test_get_all_company(self):
		list_company = self.get_all_company()
		for company in list_company:
			print(company)

	def test_get_report_by_stock_code(self):
		list_report_company = self.get_report_by_stock_code("000020")
		for report in list_report_company:
			print(report)

	def test_get_report_by_date(self):
		list_report_date = self.get_report_by_date("20181114")
		for report in list_report_date:
			print(report)

	def test_get_fact(self):
		list_fact = self.get_fact("000020", "201809")
		for fact in list_fact:
			print(fact)


if __name__ == "__main__":
	config = Config()
	with ExampleDartApi(config) as runner:
		runner.test_get_company()
		runner.test_get_all_company()
		runner.test_get_report_by_stock_code()
		runner.test_get_report_by_date()
		runner.test_get_fact()

import requests

from config import Config


class DartApiBase(object):
	token = None
	DARTAPI_URI_AUTHENTICATE = "/aam/v1/authenticate"
	DARTAPI_URI_REPORT = "/api/report/{}"
	DARTAPI_URI_REPORT_DATE = "/api/report/date/{}"
	DARTAPI_URI_COMPANY = "/api/company/{}"
	DARTAPI_URI_FACT = "/api/fact/{}/{}"

	MAX_RETRY = 5
	retry_counter = 0

	def __init__(self, local_config):
		self.config = local_config

	def __enter__(self):
		return self

	def __exit__(self, type_unused, value_unused, traceback_unused):
		pass

	# 개별 기업의 사업/분기/반기 보고서 정보를 리턴합니다.
	def get_report_by_stock_code(self, stock_code):
		url = self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_REPORT.format(stock_code)
		return self.get_content(url)

	# 해당 날짜의 사업/분기/반기 보고서 정보를 리턴합니다.
	def get_report_by_date(self, date="20190102"):
		url = self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_REPORT_DATE.format(date)
		return self.get_content(url)

	# 개별 기업 정보를 리턴합니다.
	def get_company(self, stock_code):
		url = self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_COMPANY.format(stock_code)
		return self.get_content(url)

	# 모든 기업의 정보를 리턴합니다.
	def get_all_company(self):
		url = self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_COMPANY.format("")
		return self.get_content(url)

	# 기업의 분기별 재무정보를 리턴합니다.
	def get_fact(self, stock_code, quarter):
		url = self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_FACT.format(stock_code, quarter)
		return self.get_content(url)

	def get_token(self):
		if self.token:
			return self.token
		data = {
			"username": self.config.get_env_value("DARTAPI_USER"),
			"password": self.config.get_env_value("DARTAPI_USER_PASSWORD")
		}
		headers = {"Cache-Control": "no-cache"}
		content = self.get_content(self.get_token_url(), headers, data=data)
		self.token = content["token"]
		return self.token

	def get_token_url(self):
		return self.config.get_env_value("DARTAPI_HOST") + self.DARTAPI_URI_AUTHENTICATE

	def get_content(self, url, headers={}, data=None):
		response = self.make_request(url, headers, data)
		content = self.content_with_json(response)
		return content

	def make_request(self, url, headers={}, data=None):
		print(["url", url])
		# print(["headers", headers])
		# print(["data", data])
		if not headers:
			headers = {
				"Authorization": "Bearer " + self.get_token(),
				"Content-Type": "application/json"
			}

		try:
			if data:
				response = requests.post(url, data=data, headers=headers, timeout=120, stream=False, verify=False)
			else:
				response = requests.get(url, headers=headers, timeout=120, stream=False, verify=False)
		except Exception as error:
			print(["Exception", self.retry_counter])
			print(error)
			if self.retry_counter == self.MAX_RETRY:
				print(["HIT MAX_RETRY", self.MAX_RETRY, url])
				return {}
			self.retry_counter += 1
			return self.make_request(url, headers, data)
		else:
			return response

	@staticmethod
	def content_with_json(response):
		if response and response.status_code == 200:
			return response.json()
		elif response and response.status_code == 401:
			print("401 UNAUTHORIZED", "인증 정보를 확인해주세요.")
		elif response and response.status_code == 403:
			print("403 FORBIDDEN", "인증 정보를 확인해주세요.")
		else:
			print("response else", response)
			if hasattr(response, "content"):
				print([response.content])
			return {}


if __name__ == "__main__":
	config = Config()
	with DartApiBase(config) as runner:
		company = runner.get_company("000020")
		print(company)
		list_company = runner.get_all_company()
		for company in list_company:
			print(company)

		list_report_company = runner.get_report_by_stock_code("000020")
		for report in list_report_company:
			print(report)
		list_report_date = runner.get_report_by_date("20181114")
		for report in list_report_date:
			print(report)

		list_fact = runner.get_fact("000020", "201809")
		for fact in list_fact:
			print(fact)

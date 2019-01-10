# dartapi-example
DartAPI 예제입니다.

# 환경
DartAPI 예제는 아래 환경에서 제작되었습니다.
```
python:3.6
continuumio/anaconda3:4.4.0
python-dotenv:0.6.4
```

# 설정
.env 파일에 유저와 비밀번호를 설정하세요.
```
DARTAPI_HOST = "https://www.dartapi.com"
DARTAPI_USER = "username"
DARTAPI_USER_PASSWORD = "userpassword"
```

# 실행
example.py를 실행하시면 각 API의 예제가 실행됩니다. 
```
with ExampleDartApi(config) as runner:
    runner.test_get_company()
    runner.test_get_all_company()
    runner.test_get_report_by_stock_code()
    runner.test_get_report_by_date()
    runner.test_get_fact()
```


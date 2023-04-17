
# 초기 세팅
## Swagger

### package 설치
```shell
pip install drf-yasg
```

### 메인 app 설정
#### server_dev/settings.py
```python
THIRD_PARTY_APPS: list = [
    # 중략
    "drf_yasg",
]
```

#### server_dev/urls.py
```python
schema_view = get_schema_view(
    openapi.Info(
        title="variable-maker",
        default_version="1.0.0",
        description="variable-maker API 문서",
    ),
    public=True,
)


urlpatterns = [
    # 중략
    path(
        "api/v1/",
        include(
            [
                path(
                    "swagger/schema/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="swagger-schema",
                ),
                # 중략
            ]
        ),
    ),
]
```
title: 프로젝트 이름  
default_version : 프로젝트 버전  
description : 문서 설명


## Papago api 활용

### Papago API - EndPoint & Method
|API 명 | 메서드 | EndPoint URL | Return|
|---|---|---|---|
|PapagoLanguageDetection|POST|https://naveropenapi.apigw.ntruss.com/langs/v1/dect|JSON|
|PapagoNMT|POST|https://naveropenapi.apigw.ntruss.com/nmt/v1/translation|JSON|

### Papago API - Request Header
|Key|Value|
|---|---|
|X-NCP-APIGW-API-KEY-ID|Application Key - Client ID|
|X-NCP-APIGW-API-KEY|Application Key - Client Secret|

### Papago API - Request Body
|이름|타입|
|---|---|
|source|string|
|target|string|
|text|string|

예)
```json
{
  "source": "ko",
  "target": "zh-CN",
  "text": "안녕하세요."
}
```

번역 대상 언어 코드
- ko: 한국어
- en: 영어
- zh-CN: 중국어 간체
- 등등...

text는 UTF-8 인코딩, 5000자 이하

## variable_translation - papago api 를 활용한 변수 만들기 앱

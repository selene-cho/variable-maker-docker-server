
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

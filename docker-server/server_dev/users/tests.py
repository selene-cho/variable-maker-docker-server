import requests


def main(string):

    text = string

    client_id = "kwzvitt6q7"
    client_secret = "ivU998dq6eKMnyOUe5kImyDfwgF06ILTpq2d8KBh"

    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

    val = {
        "source": "ko",
        "target": "en",
        "text": text,
    }

    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }

    response = requests.post(url, data=val, headers=headers)
    rescode = response.status_code

    if rescode == 200:
        return response.text
        # return {"result": response.text}
        # print(response.text)
    else:
        print("no")
        return {"result": response.text}


if __name__ == "__main__":
    string = "동물농장"
    result = main(string)

    print(result)
    start = result.find('"translatedText"')
    end = result.find('"engineType"')
    print(result[start + 18 : end - 2])

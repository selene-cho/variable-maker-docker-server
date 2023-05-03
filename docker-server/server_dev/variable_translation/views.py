import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TranslatedVariables
from .serializers import TranslatedVariablesSerializer


class VariableTranslate(APIView):
    """

    api/v1/variabletranslate/search/?word=search_term
    """

    def get_api_data(self, query_param):
        """
        api에서 번역해온 결과를 리턴하는 뷰
        :param query_param:
        :return:
        """
        client_id = settings.PPG_ID
        client_secret = settings.PPG_SECRET

        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

        val = {
            "source": "ko",
            "target": "en",
            "text": query_param,
        }

        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
        }

        response = requests.post(url, data=val, headers=headers)
        rescode = response.status_code

        if rescode == 200:
            raw_response_text = response.text
            start = raw_response_text.find('"translatedText"')
            end = raw_response_text.find("}}}")
            translated_variable = raw_response_text[start + 18 : end - 1]
            # print(translated_variable)
            if translated_variable.startswith("a ") or translated_variable.startswith(
                "A "
            ):
                translated_variable = translated_variable[2:]
            if translated_variable.startswith("the ") or translated_variable.startswith(
                "The "
            ):
                translated_variable = translated_variable[4:]
            if translated_variable.startswith("an ") or translated_variable.startswith(
                "An "
            ):
                translated_variable = translated_variable[3:]
            if translated_variable.endswith("."):
                translated_variable = translated_variable[
                    : len(translated_variable) - 1
                ]
            # return {"result": final_result}
            return translated_variable
        else:
            # print("no result")
            return {"result": response.text}

    def get(self, request):
        query_param = request.GET.get("word")
        if query_param:
            translated_variables = TranslatedVariables.objects.filter(
                korean_word=query_param
            )

            if not translated_variables:
                # sql에서 검색이 되지 않는다면
                # print(query_param)
                translated_variable = self.get_api_data(query_param)
                # print(translated_variable)
                TranslatedVariables.objects.create(
                    korean_word=query_param,
                    translated_variable=translated_variable,
                    count=1,
                )  # DB에 create
                serializer = TranslatedVariablesSerializer(
                    data={
                        "korean_word": query_param,
                        "translated_variable": translated_variable,
                        "count": 1,
                    }
                )
                if serializer.is_valid():
                    serializer.save()

            else:
                # 검색 횟수 증가 로직
                translated_variables[0].count = translated_variables[0].count + 1
                translated_variables[0].save()
                # 검색이 된다면
                # print(translated_variables[0].korean_word)
                # print(translated_variables[0].translated_variable)
                # serializer = TranslatedVariablesSerializer(
                #     translated_variables, many=True
                # )
                # print(translated_variables.values())

                # 아래 구문 더 고민하기!
                translated_variable = TranslatedVariables.objects.get(
                    korean_word=query_param
                )
                serializer = TranslatedVariablesSerializer(
                    translated_variable,
                )

            return Response(serializer.data)
            # return Response(status=status.HTTP_200_OK)
            # if queryset is None:
            #     print("hi")
        else:
            return Response(
                {"message": "Please provide a search query."},
                status=status.HTTP_400_BAD_REQUEST,
            )

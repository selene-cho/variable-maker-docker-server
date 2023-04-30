from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Variables, AbbreviatedVariables
from .serializers import VariablesSerializer
from variable_translation.views import VariableTranslate
import openai
import re


class VariableAbbreviate(APIView):
    """

    /api/v1/variableabbreviate/search/?word=search_term
    """

    def get_api_data(self, query_param):
        """
        openai api

        :param query_param:
        :return:
        """
        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Give me the abbreviation of the word '"
                + query_param
                + "' as a multi-numbered list",
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response["choices"][0]["text"]
        except:
            return "null"

    def isEnglishOrKorean(self, input_word) -> bool:
        """
        입력한 글자에 한글이 한글자라도 포함되는지 확인하는 함수
        한글이면 True 반환

        :param input_word:
        :return:
        """
        k_count = 0
        for character in input_word:
            if ord("가") <= ord(character) <= ord("힣"):
                k_count += 1
        if k_count >= 1:
            return True
        else:
            return False

    def get(self, request):
        query_param = request.GET.get("word")
        if query_param:
            abbreviated_variables = Variables.objects.filter(
                searched_variable=query_param
            )
            # abbreviated_variables = False

            if not abbreviated_variables:
                # sql에서 검색되지 않는 경우

                checker = self.isEnglishOrKorean(query_param)

                # 한글인지 확인
                if checker:
                    abbreviated_variable = VariableTranslate.get_api_data(
                        self, query_param
                    )
                    abbreviated_variables = self.get_api_data(abbreviated_variable)
                else:
                    abbreviated_variables = self.get_api_data(query_param)
                # print(abbreviated_variables)

                abbreviated_variables_list = re.findall(
                    r"\b\w+\b", abbreviated_variables
                )
                # print(abbreviated_variables_list)

                # 리스트안에 '.'이나 한 글자인 경우 제외
                abbreviated_variables_list = [
                    character
                    for character in abbreviated_variables_list
                    if character != "."
                ]
                abbreviated_variables_list = [
                    character
                    for character in abbreviated_variables_list
                    if len(character) > 1
                ]

                pk = Variables.objects.create(
                    searched_variable=query_param,
                    count=1,
                )
                for count in range(len(abbreviated_variables_list)):
                    # print(count)
                    AbbreviatedVariables.objects.create(
                        variable=pk,
                        abbreviated_variable=abbreviated_variables_list[count],
                    )
                abbreviated_variable = Variables.objects.get(
                    searched_variable=query_param
                )
                serializer = VariablesSerializer(
                    abbreviated_variable,
                )
            else:
                abbreviated_variables[0].count = abbreviated_variables[0].count + 1
                abbreviated_variables[0].save()
                abbreviated_variable = Variables.objects.get(
                    searched_variable=query_param
                )
                serializer = VariablesSerializer(
                    abbreviated_variable,
                )

            # return Response(status=status.HTTP_200_OK)
            return Response(serializer.data)
        else:
            return Response(
                {"message", "Please provide a search query."},
                status=status.HTTP_400_BAD_REQUEST,
            )

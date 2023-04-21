from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Variables, AbbreviatedVariables
from .serializers import VariablesSerializer
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

    def get(self, request):
        query_param = request.GET.get("word")
        if query_param:
            abbreviated_variables = Variables.objects.filter(
                searched_variable=query_param
            )
            # abbreviated_variables = False

            if not abbreviated_variables:
                # sql에서 검색되지 않는 경우
                abbreviated_variables = self.get_api_data(query_param)
                # print(abbreviated_variables)
                abbreviated_variables_list = re.findall(
                    r"\b\w+\b", abbreviated_variables
                )
                # print(abbreviated_variables_list)
                pk = Variables.objects.create(
                    searched_variable=query_param,
                    count=1,
                )
                for count in range(1, len(abbreviated_variables_list), 2):
                    # print(count)
                    AbbreviatedVariables.objects.create(
                        variable=pk,
                        abbreviated_variable=abbreviated_variables_list[count],
                    )
                # serializer = VariablesSerializer(
                #     data={
                #         "searched_variable": query_param,
                #         # "abbreviated_variable": abbreviated_variables_list,
                #         "count": 1,
                #     }
                # )
                # if serializer.is_valid():
                #     serializer.save()
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

from rest_framework import serializers
from .models import Variables, AbbreviatedVariables


class AbbreviatedVariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbbreviatedVariables
        fields = ("abbreviated_variable",)


class VariablesSerializer(serializers.ModelSerializer):
    abbreviatedVariables = AbbreviatedVariablesSerializer(
        many=True,
    )

    class Meta:
        model = Variables
        fields = (
            "searched_variable",
            "count",
            "abbreviatedVariables",
        )

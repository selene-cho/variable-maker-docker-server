from rest_framework import serializers
from .models import TranslatedVariables


class TranslatedVariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedVariables
        fields = (
            "korean_word",
            "translated_variable",
            "count",
        )

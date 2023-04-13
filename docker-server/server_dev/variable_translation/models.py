from django.db import models


class TranslatedVariables(models.Model):
    """
    번역된 단어들을 저장하는 모델
    """

    korean_word: str = models.CharField(
        max_length=50,
        help_text="한글로 입력한 단어",
    )
    translated_variable: str = models.CharField(
        max_length=50,
        help_text="번역된 결과 단어",
    )

    class Meta:
        managed: bool = True

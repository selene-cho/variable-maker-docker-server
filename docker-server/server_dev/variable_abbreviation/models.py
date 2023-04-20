from django.db import models


class Variables(models.Model):
    """
    축약할 단어들을 저장하는 모델
    """

    searched_variable: str = models.CharField(
        max_length=50,
        unique=True,
        help_text="축약하려는 단어",
    )
    count: int = models.IntegerField(
        default=1,
        help_text="단어가 검색된 횟수",
    )


class AbbreviatedVariables(models.Model):
    """
    축약될 단어들을 저장하는 모델
    """

    variable: str = models.ForeignKey(
        Variables,
        on_delete=models.CASCADE,
        related_name="abbreviatedVariables",
    )
    abbreviated_variable: str = models.CharField(
        max_length=50,
        help_text="축약된 단어",
    )

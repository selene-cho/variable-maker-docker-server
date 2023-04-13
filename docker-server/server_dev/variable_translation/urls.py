from django.urls import path
from .views import VariableTranslate


urlpatterns = [
    path("search/", VariableTranslate.as_view()),
]

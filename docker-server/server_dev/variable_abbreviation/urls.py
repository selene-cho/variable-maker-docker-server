from django.urls import path
from .views import VariableAbbreviate


urlpatterns = [
    path("search/", VariableAbbreviate.as_view()),
]

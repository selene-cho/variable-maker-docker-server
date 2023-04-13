from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="variable-maker",
        default_version="1.0.0",
        description="variable-maker API 문서",
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path(
                    "swagger/schema/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="swagger-schema",
                ),
                path("variabletranslate/", include("variable_translation.urls")),
            ]
        ),
    ),
]

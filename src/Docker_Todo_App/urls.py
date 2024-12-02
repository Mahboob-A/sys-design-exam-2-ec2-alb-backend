
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

from drf_yasg import openapi 
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="System Design Exam 03: Docker, EC2, ALB Exam Todo APP API",
        default_version="v1.0",
        description="API endpoints for Todo API",
        contact=openapi.Contact(email="connect.mahboobalam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
    # Admin 
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    
    # Doc 
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-ui"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),


    # APIs
    
    # Common APP 
    path("api/v1/common/", include("core_apps.common.urls")), 
    
    # Todo APP
    path("api/v1/app/", include("core_apps.todo.urls")), 
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


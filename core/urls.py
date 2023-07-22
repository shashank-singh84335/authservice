"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_yasg import openapi
from django.contrib import admin
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from core import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version='v1',
        description="Auth Service",
        terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="shashank.singh84335@gmail.com"),
        license=openapi.License(name="Kunatam License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('auth/v1/admin/', admin.site.urls),
    path('auth/v1/', include('authapis.urls')),
    path('auth/v1/swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('auth/v1/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
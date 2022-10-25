"""TZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.template.defaulttags import url

from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi

from pattern.views import PatternViewSet
from users.views import RegistrUserView, verify

router = DefaultRouter()
router.register('pattern', PatternViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Creatiqa API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    patterns=[path('schema/', include('TZ.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api', include(router.urls)),
    path('auth', include('djoser.urls')),
    path('registr', RegistrUserView.as_view(), name='registr'),
    path('registr/verify/<str:email>', verify, name='verify'),
    path('swagger-ui/', TemplateView.as_view(template_name='swaggerui/swaggerui.html',
                                            extra_context={'schema_url': 'openapi-schema'}),
                                            name='swagger-ui'),
    re_path(  # new
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),


]

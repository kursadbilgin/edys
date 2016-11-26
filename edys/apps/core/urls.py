"""edys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Third-Party
from rest_framework import routers


# Django
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include

# Api
from api.views import LIST, UserViewSet


# Django Rest Framework Router
router = routers.DefaultRouter()

for api in LIST:
    router.register(api[0], api[1])

urlpatterns = [

    # Default
    url(r'^admin/', admin.site.urls),

    # Django Rest Framework
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

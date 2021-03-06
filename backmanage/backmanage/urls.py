"""backmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.views.static import serve
from backmanage.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # drf 文档，title
    path('docs', include_docs_urls(title='Amir')),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', include('users.urls')),
    path('approval/', include('approval.urls')),
    path('operatorsystem/', include('operatorsystem.urls')),
]

"""test_tree_menu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('pets/<url>', TemplateView.as_view(template_name='index.html')),
    path('pets/dogs/<url>', TemplateView.as_view(template_name='index.html')),
    path('pets/cats/<url>', TemplateView.as_view(template_name='index.html')),
    path(
        'pets/dogs/shepherd/<url>',
        TemplateView.as_view(template_name='index.html')
    ),
    path(
        'cities/russia',
        TemplateView.as_view(template_name='index.html'),
        name='russia'
    ),
    path(
        'cities/russia/moscow',
        TemplateView.as_view(template_name='index.html'),
        name='moscow'
    ),
    path(
        'cities/russia/murmansk',
        TemplateView.as_view(template_name='index.html'),
        name='murmansk'
    ),
    path(
        'cities/russia/yaroslavl',
        TemplateView.as_view(template_name='index.html'),
        name='yaroslavl'
    ),
    path(
        'cities/australia',
        TemplateView.as_view(template_name='index.html'),
        name='australia'
    ),
    path(
        'cities/australia/perth',
        TemplateView.as_view(template_name='index.html'),
        name='perth'
    ),
    path(
        'cities/australia/melbourne',
        TemplateView.as_view(template_name='index.html'),
        name='melbourne'
    ),
    path(
        'cities/australia/sydney',
        TemplateView.as_view(template_name='index.html'),
        name='sydney'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

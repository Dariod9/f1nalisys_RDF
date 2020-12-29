"""f1nalisys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('rdf/', views.hello, name='hello_rdf'),
    # path('fanzone/', views.fan, name="fan"),
    # path('<int:ano>', views.season),
    path('season', views.season, name="season"),
    # path('season/<int:ano>/', views.season),
    # path('season/delete/<int:ano>/<str:title>/<str:text>', views.delete_comment),
    path('teams', views.teams, name="teams"),
    # path('teams/<int:ano>/', views.teams),
    path('drivers', views.drivers, name="drivers"),
    # path('drivers/<int:ano>/', views.drivers),
    path('tracks', views.tracks, name="tracks"),
    # path('season/<int:ano>/drivers_standings', views.drivers_standings, name="drivers_standings"),
    # path('season/<int:ano>/constructors_standings', views.constructors_standings, name="constructors_standings"),
    # path('season/<int:ano>/round/<int:round>', views.race_results, name="race_results")
]

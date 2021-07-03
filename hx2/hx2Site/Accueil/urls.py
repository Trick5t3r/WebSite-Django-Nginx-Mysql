# coding: utf8
from django.urls import path
from django.conf.urls import url
#from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings

urlpatterns = [
   path('signin/', views.autentificationPage, name='signin'),
   path('logout/', views.logout_view,  name='logout'),
   path(settings.MEDIA_URL[1:] + '<path:pathFile>', views.protectedFile_view,  name='mediaProtected'),
   path('', views.mainPage, name='mainPage'),
]

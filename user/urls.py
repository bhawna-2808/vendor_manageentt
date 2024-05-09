from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static 
from django.conf import settings
from .views import *




urlpatterns = [
    path("registeruser/", RegisterUserApiview.as_view()),
    path("login-user/", login_page, name="login_page"),
   

]
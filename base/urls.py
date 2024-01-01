# base/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_page, name='form_page'),
    path('<str:custom_path>/',
         views.redirect_custom_path,
         name='redirect_custom_path'),
]

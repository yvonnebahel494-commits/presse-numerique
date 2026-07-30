from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns=[
    path('accueil',views.indexvisiteur,name='accueilvisiteur.html'),

]
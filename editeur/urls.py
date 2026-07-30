from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns=[
path('accueil/',views.index,name='accueil.edition'),
path('login/',views.login_view,name='login'),

path('editeur_formulaire/', views.editeur_form,name='editeur'),

# path('editeur/',views.editeur_view,name='editeur'),

path('maison-edition_form/',views.maison_edition_form,name='maison_edition'),
path('dashboard_form/',views.dashboard_form,name='dashboard'),


# path('maison-edition/',views.maison_edition_view,name='maison_edition'),
]
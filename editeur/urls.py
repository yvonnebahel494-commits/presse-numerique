from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from monsite import settings
from .import views
urlpatterns=[
path('accueil/',views.index,name='accueil.edition'),
path('login/',views.login_view,name='login'),

path('editeur_formulaire/', views.editeur_form,name='editeur'),

# path('editeur/',views.editeur_view,name='editeur'),

path('maison-edition_form/',views.maison_edition_form,name='maison_edition'),
path('dashboard_form/',views.dashboard_form,name='dashboard'),
path("creer-maison/", views.creer_maison, name="creer_maison"),
path( "creer-editeur/", views.creer_editeur, name="creer_editeur"),
path( "login-editeur/", views.login_editeur,name="login_editeur"),
path("logout-editeur/",  views.logout_editeur,name="logout_editeur"),
path("articles/creer/",views.creer_article,name="creer_article"),
path("articles/modifier/<int:article_id>/",views.modifier_article,name="modifier_article"),
path("articles/supprimer/<int:article_id>/",views.supprimer_article,name="supprimer_article")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
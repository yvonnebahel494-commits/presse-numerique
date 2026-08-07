from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('editeur/',include('editeur.urls')),
    path ('lecteur/',include('lecteur.urls')),
    path ('visiteur/',include('visiteur.urls')),
]

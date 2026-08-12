from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('editeur/',include('editeur.urls')),
    path ('lecteur/',include('lecteur.urls')),
    path ('visiteur/',include('visiteur.urls')),
    path ('',include('visiteur.urls')),
]
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
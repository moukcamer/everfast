# Fango/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('upload-media/', views.upload_media, name='upload_media'),  # ⬅️ AJOUTER CETTE LIGNE
    path('apropos/', views.apropos, name='apropos'),
    path('contact/', views.contact, name='contact'),
]

# Ajouter cette ligne pour servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
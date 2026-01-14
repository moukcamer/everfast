# Fango/urls.py
from django.urls import path, include
from django.contrib import admin
from . import views
from .views import VideoListView, AudioListView, GalerieListView, ArticleDetailView, ImageListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Page d'accueil
    path('', views.accueil, name='accueil'),
    
    # Sections séparées
    path('videos/', VideoListView.as_view(), name='videos'),
    path('audios/', AudioListView.as_view(), name='audios'),
    path('galerie/', GalerieListView.as_view(), name='galerie'),
     path('images/', ImageListView.as_view(), name='image_gallery'),
    
    # Détail article
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    
    # Téléchargements
    path('download/video/<int:article_id>/', views.download_video, name='download_video'),
    path('download/audio/<int:article_id>/', views.download_audio, name='download_audio'),
    
    # Gestion de l'équipe - AJOUTEZ CES URLS
    path('equipe/upload/', views.upload_photo_equipe, name='upload_photo_equipe'),
    path('equipe/upload/<int:membre_id>/', views.upload_photo_equipe, name='edit_photo_equipe'),  # ⬅️ AJOUTER CETTE LIGNE
   
    path('equipe/crop-preview/<int:membre_id>/', views.preview_crop, name='preview_crop'),
    path('equipe/liste/', views.liste_membres_equipe, name='liste_membres_equipe'),
    
    # Recherche et statistiques
    path('recherche/', views.search_media, name='search_media'),
    path('statistiques/', views.stats_view, name='stats'),
    
    # APIs
    path('api/videos/', views.api_videos, name='api_videos'),
    path('api/audios/', views.api_audios, name='api_audios'),
    
    # Pages statiques
    path('apropos/', views.apropos, name='apropos'),
    path('contact/', views.contact, name='contact'),

    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Médias
    path('images/', views.image_gallery, name='image_gallery'),
    path('images/upload/', views.upload_image, name='upload_image'),

     # Images
    path('images/', views.image_gallery, name='image_gallery'),
    path('images/upload/', views.upload_image, name='upload_image'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
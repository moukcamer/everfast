# Fango/views.py - VERSION COMPLÈTE CORRIGÉE
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.middleware.csrf import get_token
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Article, MembreEquipe, EquipeGestion
from .forms import ArticleForm, ImageForm, CategorieForm
from .models import Article, Image, Categorie
import os
import json
from django.contrib import messages
from .models import Article, Image



def accueil(request):
    """Page d'accueil avec statistiques et sections"""
    
    # Récupérer les données
    articles = Article.objects.filter(statut='publie').order_by('-date_creation')[:6]
    images = Image.objects.all().order_by('-date_upload')[:6]
    
    # Articles avec médias spécifiques
    articles_video = Article.objects.filter(
        statut='publie',
        video__isnull=False
    ).order_by('-date_creation')[:3]
    
    articles_audio = Article.objects.filter(
        statut='publie',
        audio__isnull=False
    ).order_by('-date_creation')[:3]
    
    # Pour la galerie
    gallery_images = Image.objects.all().order_by('-date_upload')[:8]
    gallery_videos = Article.objects.filter(
        statut='publie',
        video__isnull=False
    ).order_by('-date_creation')[:4]
    gallery_audios = Article.objects.filter(
        statut='publie',
        audio__isnull=False
    ).order_by('-date_creation')[:4]
    
    # Équipe (3 premiers membres)
    config_equipe = EquipeGestion.objects.first()
    membres = MembreEquipe.objects.filter(actif=True).order_by('ordre_affichage')[:3]
    # Calcul des statistiques
    stats = {
        'articles': Article.objects.filter(statut='publie').count(),
        'images': Image.objects.count(),
        'videos': Article.objects.filter(video__isnull=False).count(),
        'audios': Article.objects.filter(audio__isnull=False).count(),
        'total': Article.objects.filter(statut='publie').count() + Image.objects.count()
    }

    
    context = {
        'titre': ' Construcam - Distributeur exclusif des produits d"etanchiété Everfast',
        'message': 'Découvrez nos contenus audio, vidéo et articles',
        'articles': articles,
        'images': images,
        'articles_video': articles_video,
        'articles_audio': articles_audio,
        'gallery_images': gallery_images,
        'gallery_videos': gallery_videos,
        'gallery_audios': gallery_audios,
        'membres': membres,
        'config_equipe': config_equipe,
        
    }
    
    return render(request, 'Fango/accueil.html', context)

   

# Fango/views.py
def article_list(request):
    """Liste de tous les articles avec filtres et onglets"""
    
    # Récupérer tous les articles publiés
    articles = Article.objects.filter(statut='publie').order_by('-date_creation')
    
    # Récupérer toutes les images
    images = Image.objects.all().order_by('-date_upload')
    
    # Articles avec médias spécifiques
    articles_video = Article.objects.filter(
        statut='publie',
        video__isnull=False
    ).order_by('-date_creation')
    
    articles_audio = Article.objects.filter(
        statut='publie',
        audio__isnull=False
    ).order_by('-date_creation')
    
    # Calculer la taille totale des images
    total_size = 0
    for image in images:
        try:
            if image.fichier:
                total_size += image.fichier.size
        except:
            pass
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    # Context
    context = {
        'articles': articles,
        'images': images,
        'articles_video': articles_video,
        'articles_audio': articles_audio,
        'articles_count': articles.count(),
        'images_count': images.count(),
        'videos_count': articles_video.count(),
        'audios_count': articles_audio.count(),
        'total_size': total_size_mb,
        'page_title': 'Articles & Images',
    }
    
    return render(request, 'Fango/article_list.html', context)

def article_detail(request, slug):
    """Détail d'un article"""
    article = get_object_or_404(Article, slug=slug, statut='publie')
    return render(request, 'Fango/article_detail.html', {'article': article})
# Fango/views.py
def image_gallery(request):
    """Galerie d'images complète"""
    images = Image.objects.all().order_by('-date_upload')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        images = images.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Calculer les statistiques
    total_size = 0
    for image in images:
        try:
            if image.fichier:
                total_size += image.fichier.size
        except:
            pass
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    # Dernier upload
    latest_upload = images.first().date_upload if images.exists() else None
    
    # Tags uniques
    all_tags = set()
    for image in images:
        if image.tags:
            tags = [tag.strip() for tag in image.tags.split(',')]
            all_tags.update(tags)
    
    # Pagination
    paginator = Paginator(images, 12)  # 12 images par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'images': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_size': total_size_mb,
        'latest_upload': latest_upload,
        'tag_count': len(all_tags),
        'tags': list(all_tags)[:10],  # Limiter à 10 tags pour l'affichage
    }
    
    return render(request, 'Fango/section/image.html', context)

def image_detail(request, pk):
    """Détail d'une image"""
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'Fango/section/image_detail.html', {'image': image})

@login_required
def article_create(request):
    """Création d'un article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.slug and article.titre:
                from django.utils.text import slugify
                article.slug = slugify(article.titre)
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'Fango/article_form.html', {'form': form})

@login_required
def upload_image(request):
    """Upload d'une image dans la galerie"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_gallery')
    else:
        form = ImageForm()
    
    return render(request, 'Fango/upload_image.html', {'form': form})
   

# ==================== FONCTION UTILITAIRE POUR TÉLÉCHARGEMENT ====================
def serve_file_download(file_path, title, file_type):
    """Fonction utilitaire pour servir les fichiers"""
    if not os.path.exists(file_path):
        return HttpResponse("Fichier introuvable", status=404)
    
    try:
        file = open(file_path, 'rb')
        response = FileResponse(file)
        
        # Déterminer le type MIME
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
        }
        
        content_type = mime_types.get(ext, 'application/octet-stream')
        response['Content-Type'] = content_type
        
        # Nom du fichier pour le téléchargement
        safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}_{file_type}{ext}"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur: {str(e)}", status=500)

# ==================== TÉLÉCHARGEMENTS ====================
def download_video(request, article_id):
    """Télécharger une vidéo"""
    article = get_object_or_404(Article, id=article_id)
    
    if not article.video:
        return HttpResponse("Aucune vidéo disponible", status=404)
    
    return serve_file_download(article.video.path, article.titre, 'video')

def download_audio(request, article_id):
    """Télécharger un audio"""
    article = get_object_or_404(Article, id=article_id)
    
    if not article.audio:
        return HttpResponse("Aucun audio disponible", status=404)
    
    return serve_file_download(article.audio.path, article.titre, 'audio')

# ==================== SECTION VIDÉOS ====================
class VideoListView(ListView):
    """
    Vue liste pour toutes les vidéos (avec pagination)
    """
    model = Article
    template_name = 'Fango/sections/videos.html'
    context_object_name = 'videos'
    paginate_by = 12  # 12 vidéos par page
    
    def get_queryset(self):
        return Article.objects.filter(video__isnull=False).order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Vidéos'
        context['video_count'] = Article.objects.filter(video__isnull=False).count()
        return context

# ==================== SECTION AUDIOS ====================
class AudioListView(ListView):
    """
    Vue liste pour tous les audios (avec pagination)
    """
    model = Article
    template_name = 'Fango/sections/audios.html'
    context_object_name = 'audios'
    paginate_by = 12  # 12 audios par page
    
    def get_queryset(self):
        return Article.objects.filter(audio__isnull=False).order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Audios'
        context['audio_count'] = Article.objects.filter(audio__isnull=False).count()
        return context


class ImageListView(ListView):
    """Vue basée sur une classe pour la liste des images"""
    model = Image
    template_name = 'Fango/section/image.html'
    context_object_name = 'images'
    paginate_by = 12  # 12 images par page
    
    def get_queryset(self):
        """Filtrage des images avec recherche"""
        queryset = Image.objects.all().order_by('-date_upload')
        
        # Recherche
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__icontains=query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Ajout de données supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        
        # Récupérer le queryset complet (sans pagination pour les stats)
        queryset = self.get_queryset()
        
        # Calculer la taille totale des images
        total_size = 0
        for image in queryset:
            try:
                if image.fichier:
                    total_size += image.fichier.size
            except:
                pass
        total_size_mb = round(total_size / (1024 * 1024), 2)
        
        # Dernier upload
        latest_upload = queryset.first().date_upload if queryset.exists() else None
        
        # Tags uniques
        all_tags = set()
        for image in queryset:
            if image.tags:
                tags = [tag.strip() for tag in image.tags.split(',')]
                all_tags.update(tags)
        
        # Recherche actuelle
        current_query = self.request.GET.get('q', '')
        
        # Ajouter les données au contexte
        context.update({
            'total_size': total_size_mb,
            'latest_upload': latest_upload,
            'tag_count': len(all_tags),
            'tags': list(all_tags)[:10],  # Limiter à 10 tags pour l'affichage
            'current_query': current_query,
            'images_count': queryset.count(),
        })
        
        return context
# ==================== GALERIE MULTIMÉDIA ====================
class GalerieListView(ListView):
    """
    Vue liste pour la galerie (tous les médias)
    """
    model = Article
    template_name = 'Fango/sections/galerie.html'
    context_object_name = 'medias'
    paginate_by = 16  # 16 médias par page
    
    def get_queryset(self):
        # Filtrer par type si spécifié dans l'URL
        media_type = self.request.GET.get('type', 'all')
        
        if media_type == 'video':
            return Article.objects.filter(video__isnull=False).order_by('-date_creation')
        elif media_type == 'audio':
            return Article.objects.filter(audio__isnull=False).order_by('-date_creation')
        else:
            # Tous les médias (vidéos OU audios)
            return Article.objects.filter(
                Q(video__isnull=False) | Q(audio__isnull=False)
            ).distinct().order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_type = self.request.GET.get('type', 'all')
        
        context['page_title'] = 'Galerie Multimédia'
        context['media_type'] = media_type
        context['video_count'] = Article.objects.filter(video__isnull=False).count()
        context['audio_count'] = Article.objects.filter(audio__isnull=False).count()
        context['total_count'] = Article.objects.filter(
            Q(video__isnull=False) | Q(audio__isnull=False)
        ).distinct().count()
        
        return context

# ==================== DÉTAIL D'UN ARTICLE ====================
class ArticleDetailView(DetailView):
    """
    Vue détaillée pour un article
    """
    model = Article
    template_name = 'Fango/sections/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Articles similaires
        articles_similaires = Article.objects.exclude(id=article.id).order_by('-date_creation')[:3]
        
        context['articles_similaires'] = articles_similaires
        return context

# ==================== VUE RECHERCHE ====================
def search_media(request):
    """
    Vue de recherche dans les médias
    """
    query = request.GET.get('q', '')
    media_type = request.GET.get('type', 'all')
    
    if query:
        # Recherche dans les titres et contenus
        results = Article.objects.filter(
            Q(titre__icontains=query) | Q(contenu__icontains=query)
        )
        
        # Filtrer par type si spécifié
        if media_type == 'video':
            results = results.filter(video__isnull=False)
        elif media_type == 'audio':
            results = results.filter(audio__isnull=False)
    else:
        results = Article.objects.none()
    
    # Pagination
    paginator = Paginator(results.order_by('-date_creation'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Résultats de recherche',
        'query': query,
        'media_type': media_type,
        'results': page_obj,
        'results_count': results.count(),
    }
    
    return render(request, 'Fango/sections/search.html', context)

# ==================== STATISTIQUES ====================
def stats_view(request):
    """
    Page de statistiques des médias
    """
    # Compter les médias par mois
    from django.db.models.functions import TruncMonth
    from django.db.models import Count
    
    # Statistiques de base
    total_articles = Article.objects.count()
    total_videos = Article.objects.filter(video__isnull=False).count()
    total_audios = Article.objects.filter(audio__isnull=False).count()
    
    # Articles par mois
    articles_by_month = Article.objects.annotate(
        month=TruncMonth('date_creation')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Vidéos par mois
    videos_by_month = Article.objects.filter(video__isnull=False).annotate(
        month=TruncMonth('date_creation')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    context = {
        'page_title': 'Statistiques',
        'total_articles': total_articles,
        'total_videos': total_videos,
        'total_audios': total_audios,
        'articles_by_month': articles_by_month,
        'videos_by_month': videos_by_month,
    }
    
    return render(request, 'Fango/sections/stats.html', context)

# ==================== API POUR AJAX ====================
def api_videos(request):
    """API JSON pour les vidéos (AJAX)"""
    videos = Article.objects.filter(video__isnull=False).order_by('-date_creation')[:20]
    
    data = []
    for video in videos:
        data.append({
            'id': video.id,
            'titre': video.titre,
            'video_url': video.video.url if video.video else None,
            'date': video.date_creation.strftime('%d/%m/%Y'),
            'has_audio': bool(video.audio),
        })
    
    return JsonResponse({'videos': data})

def api_audios(request):
    """API JSON pour les audios (AJAX)"""
    audios = Article.objects.filter(audio__isnull=False).order_by('-date_creation')[:20]
    
    data = []
    for audio in audios:
        data.append({
            'id': audio.id,
            'titre': audio.titre,
            'audio_url': audio.audio.url if audio.audio else None,
            'date': audio.date_creation.strftime('%d/%m/%Y'),
            'has_video': bool(audio.video),
        })
    
    return JsonResponse({'audios': data})

# ==================== VUES EXISTANTES ====================
@login_required
@csrf_exempt
def upload_photo_equipe(request, membre_id=None):
    """
    Vue pour uploader des photos d'équipe
    """
    if request.method == 'POST':
        try:
            # Votre code existant pour POST
            pass
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Votre code pour GET
    from .models import MembreEquipe
    role_choices = MembreEquipe.ROLE_CHOICES
    
    return render(request, 'Fango/admin/equipe_upload.html', {
        'role_choices': role_choices
    })

def apropos(request):
    """
    Vue pour la page À propos
    """
    config_equipe = EquipeGestion.objects.first()
    if not config_equipe:
        config_equipe = EquipeGestion.objects.create()
    
    membres = MembreEquipe.objects.filter(actif=True).order_by('ordre_affichage')
    
    context = {
        'config_equipe': config_equipe,
        'membres': membres,
    }
    
    return render(request, 'Fango/apropos.html', context)

def contact(request):
    """
    Vue pour la page Contact
    """
    return render(request, 'Fango/contact.html')

@login_required
@csrf_exempt
def delete_membre_equipe(request, membre_id):
    """
    Supprime complètement un membre d'équipe
    """
    if request.method == 'DELETE':
        try:
            membre = get_object_or_404(MembreEquipe, id=membre_id)
            
            # Supprimer la photo si elle existe
            if membre.photo_profil and hasattr(membre.photo_profil, 'path'):
                if os.path.exists(membre.photo_profil.path):
                    if 'default-avatar' not in membre.photo_profil.path:
                        os.remove(membre.photo_profil.path)
            
            # Supprimer le membre
            membre.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Membre supprimé avec succès'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée'
    })

@login_required
def liste_membres_equipe(request):
    """
    Affiche une liste simple des membres d'équipe en HTML
    """
    membres = MembreEquipe.objects.all().order_by('ordre_affichage', 'nom')
    csrf_token = get_token(request)
    
    # Construction du tableau HTML
    rows_html = ""
    for membre in membres:
        rows_html += f"""
        <tr>
            <td><img src="{membre.photo_url}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;"></td>
            <td><strong>{membre.prenom} {membre.nom}</strong></td>
            <td>{membre.get_role_display()}</td>
            <td>{"✅ Actif" if membre.actif else "❌ Inactif"}</td>
            <td>
                <a href="/equipe/upload/{membre.id}/" style="padding:4px 8px;background:#4CAF50;color:white;border-radius:3px;text-decoration:none;font-size:12px;">Éditer</a>
                <a href="/equipe/crop-preview/{membre.id}/" style="padding:4px 8px;background:#FF9800;color:white;border-radius:3px;text-decoration:none;margin-left:5px;font-size:12px;">Recadrer</a>
            </td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liste des membres - Fango</title>
        <style>
            body {{ font-family: Arial; max-width: 1200px; margin: 20px auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #f8f9fa; font-weight: bold; color: #555; }}
            tr:hover {{ background: #f9f9f9; }}
            .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background: #5a67d8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Liste des membres d'équipe</h1>
            <p>Total : {membres.count()} membre(s)</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Photo</th>
                        <th>Nom</th>
                        <th>Rôle</th>
                        <th>Statut</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else "<tr><td colspan='5' style='text-align:center;padding:40px;color:#666;'>Aucun membre trouvé</td></tr>"}
                </tbody>
            </table>
            
            <div style="margin-top: 30px;">
                <a href="/equipe/upload/" class="btn">➕ Ajouter un nouveau membre</a>
                <a href="/apropos/" class="btn" style="background: #6c757d; margin-left: 10px;">👈 Retour à la page d'équipe</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html)


# Vue pour prévisualiser le recadrage
@login_required
def preview_crop(request, membre_id):
    """
    Affiche l'interface de prévisualisation et recadrage
    """
    membre = get_object_or_404(MembreEquipe, id=membre_id)
    
    context = {
        'membre': membre,
        'photo_url': membre.photo_url,
    }
    
    return render(request, 'Fango/crop_preview.html', context)





   
    
    
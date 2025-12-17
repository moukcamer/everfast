# Fango/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings

def accueil(request):
    """
    Vue pour la page d'accueil
    """
    context = {
        'titre': 'Bienvenue sur mon site Fango',
        'message': 'Ceci est la page d\'accueil',
        'articles': []  # Vous pouvez remplir ceci plus tard
    }
    return render(request, 'Fango/accueil.html', context)

@csrf_exempt
def upload_media(request):
    """
    Vue pour gérer l'upload des médias (audio/vidéo)
    """
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            title = request.POST.get('title', 'Sans titre')
            description = request.POST.get('description', '')
            media_type = request.POST.get('media_type', 'video')
            media_file = request.FILES.get('media_file')
            
            if not media_file:
                return JsonResponse({
                    'success': False,
                    'error': 'Aucun fichier fourni'
                })
            
            # Déterminer le dossier de destination
            if media_type == 'video':
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
            else:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
            
            # Créer le dossier s'il n'existe pas
            os.makedirs(upload_dir, exist_ok=True)
            
            # Sauvegarder le fichier
            file_path = os.path.join(upload_dir, media_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in media_file.chunks():
                    destination.write(chunk)
            
            # Ici, vous pourriez sauvegarder en base de données
            # Pour l'instant, on retourne juste un succès
            
            return JsonResponse({
                'success': True,
                'message': 'Média téléchargé avec succès',
                'file_name': media_file.name,
                'file_url': f'/media/{media_type}s/{media_file.name}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # Si ce n'est pas une requête POST, retourner un formulaire simple
    return render(request, 'Fango/upload_form.html')

# Ajoutez d'autres vues si nécessaire
def apropos(request):
    return render(request, 'Fango/apropos.html')

def contact(request):
    return render(request, 'Fango/contact.html')
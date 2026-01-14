# Fango/models.py
from django.db import models
from django.utils.text import slugify
import os

class Article(models.Model):
    CATEGORIE_CHOICES = [
        ('news', 'Actualités'),
        ('tutorial', 'Tutoriel'),
        ('review', 'Revue'),
        ('other', 'Autre')
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé')
    ]
    
    # Champs de base
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, null=True)
    contenu = models.TextField(verbose_name="Contenu", blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    date_publication = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    
    # Médias
    image = models.ImageField(
        upload_to='articles/images/',
        blank=True,
        null=True,
        verbose_name="Image principale"
    )
    
    video = models.FileField(
        upload_to='articles/videos/',
        blank=True,
        null=True,
        verbose_name="Vidéo"
    )
    
    audio = models.FileField(
        upload_to='articles/audios/',
        blank=True,
        null=True,
        verbose_name="Audio"
    )
    
    # Informations
    auteur = models.CharField(max_length=100, blank=True, verbose_name="Auteur")
    categorie = models.CharField(
        max_length=50,
        choices=CATEGORIE_CHOICES,
        blank=True,
        verbose_name="Catégorie"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name="Statut"
    )
    
    est_en_vedette = models.BooleanField(default=False, verbose_name="En vedette")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    
    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        # Générer le slug automatiquement
        if not self.slug and self.titre:
            self.slug = slugify(self.titre)
        
        # Mettre à jour la date de publication si publié
        if self.statut == 'publie' and not self.date_publication:
            from django.utils import timezone
            self.date_publication = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def has_image(self):
        return bool(self.image)
    
    @property
    def has_video(self):
        return bool(self.video)
    
    @property
    def has_audio(self):
        return bool(self.audio)
    
    @property
    def has_media(self):
        return self.has_image or self.has_video or self.has_audio

# Fango/models.py - Modèle Image corrigé
class Image(models.Model):
    """Modèle pour les images de la galerie"""
    nom = models.CharField(max_length=200, verbose_name="Nom")
    fichier = models.ImageField(upload_to='images/', verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    date_upload = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    
    # Ajouter le champ tags s'il n'existe pas
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Tags",
        help_text="Séparés par des virgules"
    )
    
    class Meta:
        ordering = ['-date_upload']
        verbose_name = "Image"
        verbose_name_plural = "Images"
    
    def __str__(self):
        return self.nom
    

class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class MembreEquipe(models.Model):
    """
    Modèle pour les membres de l'équipe avec photo de profil
    """
    ROLE_CHOICES = [
        ('tcom', 'Technico-Commercial'),
        ('infor', 'Responsable Informatique'),
        ('Maket', 'Responsable Maketin'),
        ('admin', 'Administrateur'),
        ('other', 'Autre'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='dev')
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    # Photo de profil
  
    photo_profil = models.ImageField(
        upload_to='equipe/photos/',
        default='equipe/photos/default-avatar.png',  # Assurez-vous que cette ligne existe
        blank=True
    )
    
    date_ajout = models.DateTimeField(auto_now_add=True)
    ordre_affichage = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['ordre_affichage', 'nom']
        verbose_name = "Membre d'équipe"
        verbose_name_plural = "Membres d'équipe"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def photo_url(self):
        """Retourne l'URL de la photo ou une image par défaut"""
        if self.photo_profil and hasattr(self.photo_profil, 'url'):
            return self.photo_profil.url
        return '/static/images/default-avatar.png'
    
    def save(self, *args, **kwargs):
        # Supprimer l'ancienne photo si elle existe et si elle n'est pas la photo par défaut
        if self.pk:
            try:
                ancien = MembreEquipe.objects.get(pk=self.pk)
                if ancien.photo_profil != self.photo_profil:
                    if ancien.photo_profil and os.path.isfile(ancien.photo_profil.path):
                        if 'default-avatar' not in ancien.photo_profil.path:
                            os.remove(ancien.photo_profil.path)
            except MembreEquipe.DoesNotExist:
                pass
        super().save(*args, **kwargs)

class EquipeGestion(models.Model):
    """
    Gestion des paramètres de la section équipe
    """
    titre_section = models.CharField(max_length=200, default="Notre Équipe")
    description_section = models.TextField(
        default="Découvrez notre équipe passionnée et dévouée qui travaille chaque jour pour vous offrir la meilleure expérience."
    )
    afficher_photos = models.BooleanField(default=True)
    afficher_reseaux = models.BooleanField(default=True)
    nombre_par_ligne = models.IntegerField(
        default=4,
        choices=[(2, '2'), (3, '3'), (4, '4'), (6, '6')]
    )
    
    def __str__(self):
        return "Configuration de l'équipe"
    
    class Meta:
        verbose_name = "Configuration équipe"
        verbose_name_plural = "Configuration équipe"

    

# Fango/admin.py
from django.contrib import admin
from .models import Article, Image, Categorie

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'count_articles')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)
    
    def count_articles(self, obj):
        return obj.article_set.count()
    count_articles.short_description = "Nombre d'articles"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'titre', 
        'display_auteur', 
        'display_categorie', 
        'statut',
        'has_image_display', 
        'has_video_display', 
        'has_audio_display',
        'date_publication_display', 
        'est_en_vedette'
    )
    list_filter = (
        'statut', 
        'categorie',
        'est_en_vedette',
        'date_creation',  # Utiliser date_creation au lieu de date_publication si nécessaire
    )
    list_editable = ('statut', 'est_en_vedette')
    search_fields = ('titre', 'contenu', 'auteur_nom', 'auteur__username')
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = (
        'date_creation', 
        'date_modification',
        # 'date_publication' retiré car il ne devrait pas être en readonly
    )
    
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'contenu', 'meta_description', 'mots_cles')
        }),
        ('Médias', {
            'fields': ('image', 'video', 'audio'),
            'classes': ('collapse',)  # Optionnel: rendre ce fieldset pliable
        }),
        ('Catégorisation', {
            'fields': ('categorie', 'ancienne_categorie')
        }),
        ('Publication', {
            'fields': (
                'auteur', 
                'auteur_nom',
                'statut', 
                'est_en_vedette',
                'date_publication'
            )
        }),
        ('Dates (automatiques)', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    # Méthodes personnalisées pour l'affichage
    def display_auteur(self, obj):
        return obj.nom_auteur
    display_auteur.short_description = "Auteur"
    
    def display_categorie(self, obj):
        return obj.nom_categorie
    display_categorie.short_description = "Catégorie"
    
    def has_image_display(self, obj):
        return obj.has_image
    has_image_display.boolean = True
    has_image_display.short_description = "Image"
    
    def has_video_display(self, obj):
        return obj.has_video
    has_video_display.boolean = True
    has_video_display.short_description = "Vidéo"
    
    def has_audio_display(self, obj):
        return obj.has_audio
    has_audio_display.boolean = True
    has_audio_display.short_description = "Audio"
    
    def date_publication_display(self, obj):
        if obj.date_publication:
            return obj.date_publication.strftime("%d/%m/%Y %H:%M")
        return "Non publié"
    date_publication_display.short_description = "Date publication"
    
    # Pour le tri par date_publication
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('auteur', 'categorie')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_upload', 'display_extension', 'preview')
    list_filter = ('date_upload',)
    search_fields = ('nom', 'description', 'tags')
    readonly_fields = ('date_upload', 'preview')
    
    fieldsets = (
        ('Image', {
            'fields': ('nom', 'fichier', 'preview')
        }),
        ('Description', {
            'fields': ('description', 'tags')
        }),
        ('Métadonnées', {
            'fields': ('date_upload',),
            'classes': ('collapse',)
        }),
    )
    
    def display_extension(self, obj):
        return obj.extension
    display_extension.short_description = "Format"
    
    def preview(self, obj):
        if obj.fichier:
            return f'<img src="{obj.fichier.url}" style="max-height: 100px;" />'
        return "Aucune image"
    preview.allow_tags = True
    preview.short_description = "Aperçu"
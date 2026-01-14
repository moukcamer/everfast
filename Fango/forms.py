
from django import forms
from .models import Article, Image, Categorie
from django.utils import timezone


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'titre', 'contenu', 'image', 'video', 'audio',
            'auteur', 'categorie', 'statut', 'est_en_vedette'
        ]
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'article'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Contenu de l\'article...'
            }),
            'auteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'auteur'
            }),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['nom', 'fichier', 'description', 'tags']  # Inclure tags ici
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'image'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de l\'image...'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tag1, tag2, tag3...'
            }),
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
        }
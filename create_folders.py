import os

# Liste des dossiers à créer
folders = [
    'media/videos',
    'media/audio',
    'media/uploads',
    'static/css',
    'static/js',
    'static/images'
]

print("Création des dossiers...")
for folder in folders:
    try:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Dossier créé : {folder}")
    except Exception as e:
        print(f"✗ Erreur pour {folder} : {e}")

print("\nStructure créée :")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 4 * level
    print(f'{indent}{os.path.basename(root)}/')
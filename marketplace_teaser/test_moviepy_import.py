# test_moviepy_import.py
try:
    import moviepy.editor
    print("Importation de moviepy.editor réussie !")
    
    # Test minimal de création de clip
    from moviepy.editor import TextClip, ColorClip, concatenate_videoclips
    
    # Créer un clip texte simple
    clip = TextClip("Test MoviePy", fontsize=70, color='white')
    
    print("Création de clip réussie !")
except Exception as e:
    print(f"Erreur lors de l'importation ou de la création de clip : {e}")
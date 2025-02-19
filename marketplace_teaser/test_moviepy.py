import moviepy
import importlib
import sys

def debug_moviepy_import():
    print("Python executable:", sys.executable)
    print("\nChemins de recherche de modules:")
    for path in sys.path:
        print(path)

    try:
        # Importation explicite des composants
        from moviepy.video.VideoClip import VideoClip
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        from moviepy.video.io.VideoFileClip import VideoFileClip
        from moviepy.video.tools.drawing import color_gradient
        
        # Vérification des chemins
        print("\nChemins des modules MoviePy:")
        print("VideoClip:", VideoClip.__module__)
        print("CompositeVideoClip:", CompositeVideoClip.__module__)
        print("VideoFileClip:", VideoFileClip.__module__)
        
        # Tentative d'importation des éditeurs
        import moviepy.video.editor
        import moviepy.audio.editor
        
        print("\nModules editor importés avec succès")
    
    except Exception as e:
        print(f"Erreur d'importation : {e}")
        
        # Liste détaillée des modules disponibles
        print("\nModules disponibles dans MoviePy:")
        for name, module in list(sys.modules.items()):
            if 'moviepy' in str(name):
                print(name)

debug_moviepy_import()
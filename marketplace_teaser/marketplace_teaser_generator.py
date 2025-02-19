# marketplace_teaser_generator.py
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import math

class ExpatMarketplaceTeaserGenerator:
    def __init__(self, output_path='expatriates_marketplace_teaser.mp4', width=1920, height=1080):
        """
        Générateur de teaser pour marketplace d'expatriés
        """
        self.output_path = output_path
        self.width = width
        self.height = height
        
        # Configuration de la sortie vidéo
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_path, self.fourcc, 24.0, (width, height))
        
        # Dossier pour les ressources
        self.resources_folder = 'marketplace_teaser_resources'
        os.makedirs(self.resources_folder, exist_ok=True)
    
    def create_background(self, color=(255,255,255)):
        """
        Crée un fond uni
        """
        return np.full((self.height, self.width, 3), color, dtype=np.uint8)
    
    def draw_stick_figure(self, image, x, y, height=200, is_seller=True):
        """
        Dessine une silhouette de personnage simple
        """
        color = (0, 0, 255) if is_seller else (0, 255, 0)
        
        # Tête
        cv2.circle(image, (x, y - height), height // 6, color, -1)
        
        # Corps
        cv2.line(image, (x, y - height + height // 6), 
                 (x, y - height // 3), color, 10)
        
        # Bras
        cv2.line(image, (x, y - height // 2), 
                 (x - height // 3, y - height // 3), color, 10)
        cv2.line(image, (x, y - height // 2), 
                 (x + height // 3, y - height // 3), color, 10)
        
        # Jambes
        cv2.line(image, (x, y - height // 3), 
                 (x - height // 4, y), color, 10)
        cv2.line(image, (x, y - height // 3), 
                 (x + height // 4, y), color, 10)
        
        return image
    
    def add_text(self, image, text, position, font_size=50, color=(0,0,0)):
        """
        Ajoute du texte à l'image
        """
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        draw.text(position, text, font=font, fill=color)
        
        return np.array(pil_image)
    
    def create_item_image(self, text="Meuble à vendre"):
        """
        Crée une image représentant un objet à vendre
        """
        image = np.full((300, 400, 3), (200, 200, 200), dtype=np.uint8)
        image = self.add_text(image, text, (50, 100), font_size=30)
        return image
    
    def create_handshake_scene(self):
        """
        Scène de poignée de main
        """
        frames = []
        
        for i in range(24 * 3):  # 3 secondes
            scene = self.create_background()
            
            # Personnages
            scene = self.draw_stick_figure(scene, self.width // 3, self.height, is_seller=True)
            scene = self.draw_stick_figure(scene, 2 * self.width // 3, self.height, is_seller=False)
            
            # Animation de rapprochement
            offset = int(i * (self.width // 6) / (24 * 3))
            
            # Poignée de main progressive
            if i > 12:
                cv2.line(scene, 
                         (self.width // 3 + offset, self.height - self.height // 2),
                         (2 * self.width // 3 - offset, self.height - self.height // 2), 
                         (100, 100, 100), 20)
            
            # Texte explicatif
            scene = self.add_text(scene, "Transaction Réussie !", 
                                  (self.width // 2 - 200, 100), 
                                  font_size=70)
            
            frames.append(scene)
        
        return frames
    
    def create_sale_preparation_scene(self):
        """
        Scène de préparation de la vente
        """
        frames = []
        item = self.create_item_image()
        
        for i in range(24 * 3):  # 3 secondes
            scene = self.create_background()
            
            # Personnage vendeur
            scene = self.draw_stick_figure(scene, self.width // 2, self.height, is_seller=True)
            
            # Déplacer l'objet
            x_offset = int(i * (self.width // 2) / (24 * 3))
            scene[100:400, x_offset:x_offset+400] = item
            
            # Texte
            scene = self.add_text(scene, "Préparation de la Vente", 
                                  (self.width // 2 - 200, 50), 
                                  font_size=70)
            
            frames.append(scene)
        
        return frames
    
    def create_whatsapp_scene(self):
        """
        Scène de conversation WhatsApp
        """
        frames = []
        
        for i in range(24 * 3):  # 3 secondes
            scene = self.create_background((230, 255, 210))  # Fond vert WhatsApp
            
            # Dessiner des bulles de dialogue
            bubble_height = 200
            margin = 50
            
            # Bulle de gauche (acheteur)
            cv2.rectangle(scene, 
                          (margin, self.height - bubble_height - margin), 
                          (self.width // 2 - margin, self.height - margin), 
                          (255, 255, 255), -1)
            
            # Bulle de droite (vendeur)
            cv2.rectangle(scene, 
                          (self.width // 2 + margin, self.height - bubble_height - margin), 
                          (self.width - margin, self.height - margin), 
                          (202, 246, 156), -1)
            
            # Texte dans les bulles
            scene = self.add_text(scene, "Intéressé par votre annonce", 
                                  (margin + 20, self.height - bubble_height), 
                                  font_size=40)
            scene = self.add_text(scene, "Prix négociable ?", 
                                  (self.width // 2 + margin + 20, self.height - bubble_height), 
                                  font_size=40)
            
            # Titre de la scène
            scene = self.add_text(scene, "Négociation en Cours", 
                                  (self.width // 2 - 200, 50), 
                                  font_size=70)
            
            frames.append(scene)
        
        return frames
    
    def generate_marketplace_teaser(self):
        """
        Génère le teaser vidéo complet
        """
        # Scènes
        scenes = [
            self.create_sale_preparation_scene(),
            self.create_whatsapp_scene(),
            self.create_handshake_scene()
        ]
        
        # Écrire toutes les frames
        for scene in scenes:
            for frame in scene:
                self.out.write(frame)
        
        # Libérer la ressource de sortie vidéo
        self.out.release()
        
        print(f"Teaser vidéo généré : {self.output_path}")

# Utilisation
if __name__ == "__main__":
    teaser_generator = ExpatMarketplaceTeaserGenerator()
    teaser_generator.generate_marketplace_teaser()
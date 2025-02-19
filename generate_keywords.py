import random
import os

def generate_misspelled_sentences(base_keywords, num_variations=15):
    variations = set()
    
    for keyword in base_keywords:
        variations.update([
            f'"{keyword}"',
            f'"{keyword.replace("hello", "helo")}"' if "hello" in keyword else f'"{keyword}"',
            f'"{keyword.replace("hi", "hii")}"' if "hi" in keyword else f'"{keyword}"',
            f'"{keyword.replace("hey", "heyy")}"' if "hey" in keyword else f'"{keyword}"',
            f'"{keyword.replace("bonjour", "bonjor")}"' if "bonjour" in keyword else f'"{keyword}"',
            f'"{keyword.replace("salam", "salm")}"' if "salam" in keyword else f'"{keyword}"',
            f'"{keyword.replace("salut", "slt")}"' if "salut" in keyword else f'"{keyword}"',
            f'"{keyword.replace("good morning", "gud morning")}"' if "good morning" in keyword else f'"{keyword}"',
            f'"{keyword.replace("good evening", "gud evening")}"' if "good evening" in keyword else f'"{keyword}"',
            f'"{keyword.replace("how are you", "hw r u")}"' if "how are you" in keyword else f'"{keyword}"'
        ])
    
    variations = list(variations)  # Convertir en liste
    random_sentences = set()
    
    while len(random_sentences) < min(num_variations, len(variations)):
        sentence_words = random.sample(variations, k=min(len(variations), random.randint(1, 3)))
        sentence = ", ".join(sorted(set(sentence_words)))  # Éviter répétition dans une phrase
        random_sentences.add(sentence)
    
    return list(random_sentences)

if __name__ == "__main__":
    # Liste de mots-clés de base avec erreurs possibles
    base_keywords = [
        "hi", "hello", "hey", "bonjour", "salam", "salut", "good morning", "good evening", "how are you"
    ]
    
    results = generate_misspelled_sentences(base_keywords)
    file_path = "generated_keywords.txt"
    
    with open(file_path, "w") as f:
        f.write(", \n".join(results))
    
    print("Results saved to generated_keywords.txt")
    os.system(f'start {file_path}')

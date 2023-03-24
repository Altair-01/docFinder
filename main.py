import os
import re
from PyPDF2 import PdfReader
from collections import Counter
import shutil
# Chemin vers le dossier contenant les fichiers PDF
pdf_dir = "/Users/user/Desktop/pdf/"
dest_dir = "/Users/user/Desktop/pdf/matching_files/"
#Renseigner les mots recherchés
search_words = input("Entrez les mots de recherche, séparés par des virgules : ")
search_words = search_words.split(",")
# Compter les mots
nbr_mots = 0

# Initialize a Counter object to store the word counts
word_counts = Counter()

#Stockage des noms de fichiers
matching_files = []

# Parcours de tous les fichiers dans le dossier
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        print(filename)
        # Ouverture du fichier PDF en mode lecture binaire
        with open(os.path.join(pdf_dir, filename), "rb") as pdf_file:
            # Création d'un objet PDFReader
            reader = PdfReader(pdf_file)

            #extraire le text
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                #print(page.extract_text())
                text = page.extract_text()

                all_words_found = True  # Initialiser à True
                # If the page has text, count the number of words
                # Search for the search words in the text
                for word in search_words:
                    if word.lower() not in text.lower():
                        all_words_found = False
                        break
                if all_words_found and filename not in matching_files:
                    matching_files.append(filename)
                if text:
                    # Split the text into words and count the number of words
                    words = re.findall(r"\b\w+(?:[-'\(]\w+[\)'])*\b", text)
                    word_count = len(words)                    # Add the word count of the page to the total word count
                    nbr_mots += word_count
                    # Split the text into words and update the Counter object
                    word_counts.update(text.split())

# Print the total word count
print(f"Nombre total de mots: {sum(word_counts.values())}")

# Print the word counts
#for word, count in word_counts.items():
   # print(f"{word}: {count}")

#Renvoyer les fichiers où se trouvent ces mots
if matching_files:
    print("Fichiers correspondants :")
    for filename in matching_files:
        print(filename)
        shutil.move(os.path.join(pdf_dir, filename), os.path.join(dest_dir, filename))
else:
    print("Aucun fichier ne correspond à la recherche.")
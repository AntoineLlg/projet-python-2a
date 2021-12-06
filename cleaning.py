import pandas as pd
import re

data = pd.read_csv("./comments.csv")

# Fonction de nettoyage très light. Si on veut plus nettoyer, utiliser le module re, voir dans liens utiles/NLP

def cleaning(text):
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    return text


# ajout d'une colonne à data avec le texte nettoyé

data[["textClean"]] = data[["textOriginal"]].apply(cleaning)
import numpy as np
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import nltk

nltk.download('punkt')


def blober(text: str) -> float:
    """
    Calcule la polarité d'un texte.

    Paramètres :
    ----------
    text : str
        texte dont on veut mesurer la polarité

    Sortie :
    ----------
    float
        polarisation : score entre -1 et 1.
        Plus le score est proche de 1, plus le commentaire est positif.
        Plus il est proche de -1, plus le commentaire est négatif.
    """
    return TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]


blober = np.vectorize(blober)


def sentences(comment: str) -> list:
    """
    Découpe un texte en phrases.

    Paramètres :
    ----------
    comment : str
        texte dont on veut extraire les phrases

    Sortie :
    ----------
    list[str]
        liste des phrases du texte
    """
    tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
    return tokenizer.tokenize(comment)


def polarisation(comment: str) -> float:
    """
    Calcule la polarisation d'un commentaire en calculant d'abord la polarisation de chacune de ses
    phrases et en en faisant la moyenne

    Paramètres :
    ----------
    comment : str
        texte dont on veut la polarisation

    Sortie :
    ----------
    float
        moyenne des polarisations des phrases du texte
    """
    s = sentences(comment)
    return blober(s).mean()


polarisation = np.vectorize(polarisation)

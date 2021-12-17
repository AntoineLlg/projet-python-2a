# # Polarisation des commentaires


#!pip install textblob
#!pip install textblob-fr


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

#import le dataframe avec la colonne clean
data = pd.read_csv('comments.csv')


# Il faudrait faire l'analyse phrase par phrase, et pas commentaire par commentaire.

def blober(text):
    return TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]

blober = np.vectorize(blober)
data["Polarity"] = data.loc[:,['textClean']].apply(blober)

fig = data["Polarity"].plot.bar()
plt.show()

#Tests sur la commande TextBlob

text = data.textClean[102]
print(text)
print(TextBlob(text, pos_tagger = PatternTagger(), analyzer = PatternAnalyzer()).sentiment[0])
blob = TextBlob(text)
print(blob.sentiment)


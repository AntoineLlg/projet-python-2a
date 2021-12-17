import pandas
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy

data = pd.read_csv("./comments.csv")

data["textClean"] = data.loc[:, ["textOriginal"]]
data["textClean"] = data["textClean"].str.lower().replace('\n', ' ').replace('\r', '')

data.to_csv(path_or_buf='./comments.csv',
            index=False)
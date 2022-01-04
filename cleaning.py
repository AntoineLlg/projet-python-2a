import pandas as pd


data = pd.read_csv("./comments.csv")

data["textClean"] = data.loc[:, ["textOriginal"]]
# on retire les retours à la ligne et on passe tout les caractères en minuscules
data["textClean"] = data["textClean"].str.lower().replace('\n', ' ').replace('\r', '')

data.to_csv(path_or_buf='./comments.csv',
            index=False)

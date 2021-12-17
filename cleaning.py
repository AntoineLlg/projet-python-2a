import pandas as pd


data = pd.read_csv("./comments.csv")

data["textClean"] = data.loc[:, ["textOriginal"]]
data["textClean"] = data["textClean"].str.lower().replace('\n', ' ').replace('\r', '')

data.to_csv(path_or_buf='./comments.csv',
            index=False)
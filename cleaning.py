import pandas as pd

data = pd.read_csv("./comments.csv")

text = data[["textDisplay"]][0]
text = text.lower()
text
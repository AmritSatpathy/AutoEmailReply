import pandas as pd


def merge():
    a = pd.read_csv("finedresult.csv")
    b = pd.read_csv("predictedresult.csv", engine="python")
    out = a.append(b)
    with open('result.csv', 'w', encoding='utf-8') as f:
        out.to_csv(f, index=False)
    col_list = ['From', 'Subject', 'text/plain', 'Label']
    df = pd.read_csv("result.csv", usecols=col_list)
    df.to_csv('finedresult.csv')

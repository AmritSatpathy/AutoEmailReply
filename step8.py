import pandas as pd
import en_core_web_sm
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup

STOPWORDS = set(stopwords.words('english'))
nlp = en_core_web_sm.load()


def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', str(text))


def html(text):
    return BeautifulSoup(text, "lxml").text


def sentclean():
    df = pd.read_json(r'all_emailsent.json')
    df.to_csv(r'fromsentjson.csv', index=None)
    col_list = ['Subject', 'text/plain', 'From']
    df = pd.read_csv("fromsentjson.csv", usecols=col_list)
    df.drop(df[df['Subject'] == ('Delivery Status Notification (Failure)')].index, inplace=True)
    df.drop(df[df['Subject'] == ('Delivery Status Notification (Delay)')].index, inplace=True)
    patternDel = ".*Undeliverable.*"
    patternDel1 = ".*[M,m]ail [D,d]elivery .*[S,s]ystem.*"
    filter = df['Subject'].str.contains(patternDel)
    df = df[~filter]
    filter = df['From'].str.contains(patternDel1)
    df = df[~filter]
    df['text/plain'] = df['text/plain'].replace(to_replace=[">.*\n"], value=[""], regex=True)
    df['text/plain'] = df['text/plain'].replace(to_replace=
                                                ["---------- Forwarded message ---------", "Hey .*\n", "Hi .*\n",
                                                 "[E,e]mail.[1,2,3,4,5,6,7,8,9,0]", "From:.*\n", "Subject:.*\n", "-",
                                                 ".*<.*", ".*wrote:.*\n"],
                                                value=["", "", "", "", "", "", "", "", ""], regex=True)
    df = df.dropna()
    df["text/plain"] = df["text/plain"].apply(remove_urls)
    df['text/plain'] = df['text/plain'].apply(html)
    # df["text/plain"] = df["text/plain"].apply(stopwords)
    # f['text/plain'] = df['text/plain'].str.replace('[^\w\s]','')
    df = df.replace(to_replace=[r"\\n|\\r", "\n|\r"], value=["", ""], regex=True)
    df['text/plain'] = df['text/plain'].replace(
        to_replace=["About Us.*", "[B,b]est", "D[i,I][S,s][c,C][l,L][a,A][i,I][M,m][E,e][r,R].*", "[r,R]egards",
                    "[T,t][H,h][a,A][n.N][K,k][s,S]."],
        value=["", "", "", "", ""], regex=True)
    df.to_csv('cleanedsent.csv')


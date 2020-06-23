import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
def load():
    train = pd.read_csv("finedresult.csv", engine='python')
    x = train['text/plain']
    vectorizer = CountVectorizer()
    wordvec = vectorizer.fit(x.values.astype('U'))
    data = pd.read_csv("cleaned.csv", engine='python')
    df = pd.DataFrame(data)
    x_train = data['text/plain']
    with open('botmodel.mod', 'rb') as f:
        model = pickle.load(f)
    prediction = model.predict_classes(vectorizer.transform(x_train))
    df['Label'] = prediction
    df.to_csv(r'predictedresult.csv',index=False)

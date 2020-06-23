from keras.models import Sequential
from keras.layers import Dense
import sklearn.model_selection as model_selection
from sklearn.feature_extraction.text import CountVectorizer
from warnings import filterwarnings
import pickle
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True

filterwarnings('ignore')
import numpy as np
import pandas as pd


def nlp():
    seed = 7
    np.random.seed(seed)
    train = pd.read_csv("finedresult.csv", engine='python')
    x = train['text/plain']
    y = train['Label']
    train_x, test_x, train_y, test_y = model_selection.train_test_split(x, y, test_size=0.2, random_state=1)
    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(x, y, test_size=0.25, random_state=1)
    vectorizer = CountVectorizer()
    vectorizer.fit(x.values.astype('U'))
    x_train_count = vectorizer.transform(train_x.values.astype('U'))
    x_valid_count = vectorizer.transform(valid_x.values.astype('U'))
    x_test_count = vectorizer.transform(test_x.values.astype('U'))
    model = Sequential()
    model.add(Dense(50, input_dim=x_train_count.shape[1], kernel_initializer="uniform", activation="relu"))
    model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x_train_count, train_y.values.reshape(-1, 1), validation_data=(x_valid_count, valid_y),nb_epoch=50, batch_size=128)
    loss, acc = model.evaluate(x_test_count, test_y, verbose=0)
    print('Test Accuracy: %f' % (acc * 100))
    with open('botmodel.mod', 'wb') as m:
        pickle.dump(model, m)




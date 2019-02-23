from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap


from sklearn import svm
from sklearn import datasets
from sklearn.model_selection import train_test_split as ts
from sklearn import cross_validation, ensemble, preprocessing, metrics
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
Bootstrap(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    if request.method == 'POST':
        namequery = request.form['namequery']
        X_test_sparse_matrix = count_vect.transform([namequery])
        X_test_tfidf = tfidf_transformer.fit_transform(X_test_sparse_matrix)
        predicted = clf.predict(X_test_tfidf)
        my_prediction = predicted[0]

	
    return render_template('results.html',prediction = my_prediction,name = namequery.upper())

stores = [{
    'name': 'storeA',
    'items': [{'name':'my item 1', 'price': 30 }],
    },
    {
    'name': 'storeB',
    'items': [{'name':'my item 2', 'price': 15 }],
    },
]

@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
        return jsonify ({'message': 'store not found'})


if __name__ == '__main__':
    
    file = pd.read_csv('data/names_dataset.csv')
    word_list = []
    gender_list = []
    for i in file.values:
        word_list.append(i[1])
        gender_list.append(i[2])
    
    for i in range(len(gender_list)):
        if gender_list[i]=='M':
            gender_list[i]=0
        else:
            gender_list[i]=1
    

    X_train, X_test, Y_train, Y_test = ts(word_list, gender_list,test_size=0.2, random_state=42)

    count_vect = CountVectorizer()
    X_train_sparse_matrix = count_vect.fit_transform(X_train)
    
    dense_numpy_matrix = X_train_sparse_matrix.todense()

    from sklearn.feature_extraction.text import TfidfTransformer

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_sparse_matrix)

    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB().fit(X_train_tfidf, Y_train)

    app.run(debug=True)
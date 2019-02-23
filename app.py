from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap

import os
from sklearn.externals import joblib


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('challenge.html')


@app.route('/url-detect', methods=["GET",'POST'])
def predict():
    if request.method == "GET":
        return render_template('url_input.html')
    if request.method == 'POST':
        pass


# namequery = request.form['namequery']
# X_test_sparse_matrix = count_vect.transform([namequery])
# X_test_tfidf = tfidf_transformer.fit_transform(X_test_sparse_matrix)
# predicted = clf.predict(X_test_tfidf)
# my_prediction = predicted[0]

# return render_template('results.html',prediction = my_prediction,name = namequery.upper())

if __name__ == '__main__':
    vectorizer = joblib.load('./machine_learning_model/url_detection/my_model.pkl')
    model = joblib.load('./machine_learning_model/url_detection/my_model.pkl')

    app.run(debug=True)

from flask import Flask, render_template, request, url_for, jsonify, redirect
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
        return render_template('url-input.html')

    req = request.values
    resp = {"code":200, 'msg':"提交成功","data":{}}
    url = req['url'] if 'url' in req else ''


    if not url:
        resp['code'] = -1
        resp['msg'] = "请输入符合格式的网址"
        return jsonify(resp)

    url_vector = vectorizer.transform([url])
    predicted = model.predict(url_vector)
    app.logger.error(predicted)
    link = url_for('result', url=url, result=predicted[0])
    resp['link'] = str(link)
    return jsonify(resp)
    #return jsonify(resp)
    #return render_template('url-detect-result.html')

@app.route('/url-detect-result')
def result():
    req = request.values
    resp_data = {}
    result_id = req['result'] if 'result' in req else ''
    test_link = req['url'] if 'url' in req else ''
    if not result_id or not test_link:
        return redirect('/')

    resp_data['test_link'] = test_link
    resp_data['result_id'] = result_id

    return render_template('url-detect-result.html',test_link=test_link, result_id=result_id)

# namequery = request.form['namequery']
# X_test_sparse_matrix = count_vect.transform([namequery])
# X_test_tfidf = tfidf_transformer.fit_transform(X_test_sparse_matrix)
# predicted = clf.predict(X_test_tfidf)
# my_prediction = predicted[0]

# return render_template('results.html',prediction = my_prediction,name = namequery.upper())

if __name__ == '__main__':
    from sklearn.externals import joblib
    vectorizer = joblib.load('./machine_learning_model/url_detection/vectroizer.pkl')
    model = joblib.load('./machine_learning_model/url_detection/my_model.pkl')

    app.run(debug=True)

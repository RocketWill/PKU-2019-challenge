from flask import Flask, render_template, request, url_for, jsonify, redirect
from flask_bootstrap import Bootstrap
import os
from sklearn.externals import joblib


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url-detect', methods=["GET",'POST'])
def urlPredict():
    if request.method == "GET":
        return render_template('url-detect-input.html')

    req = request.values
    resp = {"code":200, 'msg':"提交成功","data":{}}
    url = req['url'] if 'url' in req else ''


    if not url:
        resp['code'] = -1
        resp['msg'] = "请输入符合格式的网址"
        return jsonify(resp)

    vectorizer, model = loadUrlDetect()
    url_vector = vectorizer.transform([url])
    predicted = model.predict(url_vector)
    app.logger.error(predicted)
    link = url_for('urlResult', url=url, result=predicted[0])
    resp['link'] = str(link)
    return jsonify(resp)
    #return jsonify(resp)
    #return render_template('url-detect-result.html')

@app.route('/url-detect-result')
def urlResult():
    req = request.values
    resp_data = {}
    result_id = req['result'] if 'result' in req else ''
    test_link = req['url'] if 'url' in req else ''
    if not result_id or not test_link:
        return redirect('/')

    resp_data['test_link'] = test_link
    resp_data['result_id'] = int(result_id)

    return render_template('url-detect-result.html', **resp_data)

@app.route('/domain-name', methods=["GET",'POST'])
def domainPredict():
    if request.method == "GET":
        return render_template('domain-name-input.html')

    req = request.values
    resp = {"code": 200, 'msg': "提交成功", "data": {}}
    domain_name = req['domain_name'] if 'domain_name' in req else ''

    if not domain_name:
        resp['code'] = -1
        resp['msg'] = "请输入符合格式的域名"
        return jsonify(resp)

    vectorizer, model = loadDomainModel()
    domain_name_vector = vectorizer.transform([domain_name])
    predicted = model.predict(domain_name_vector)
    app.logger.error(predicted)
    link = url_for('domainResult', domain_name=domain_name, result=predicted[0])
    app.logger.error(link)
    resp['link'] = str(link)
    return jsonify(resp)

@app.route('/domain-name-result')
def domainResult():
    req = request.values
    resp_data = {}
    result_id = req['result'] if 'result' in req else ''
    test_link = req['domain_name'] if 'domain_name' in req else ''
    if not result_id or not test_link:
        return redirect('/')

    resp_data['test_link'] = test_link
    resp_data['result_id'] = int(result_id)

    return render_template('domain-name-result.html', **resp_data)

@app.route('/adfa-ld', methods=["GET",'POST'])
def adfaldPredict():
    if request.method == "GET":
        return render_template('ADFA-LD/adfald-input.html')

    req = request.values
    resp = {"code": 200, 'msg': "提交成功", "data": {}}
    adfa_ld = req['adfa_ld'] if 'adfa_ld' in req else ''

    if not adfa_ld:
        resp['code'] = -1
        resp['msg'] = "请输入符合格式的 systemcall api"
        return jsonify(resp)

    vectorizer, model, transformer = loadADFALD()

    adfa_ld = [adfa_ld]
    adfa_ld_vector = vectorizer.transform(adfa_ld)
    adfa_ld_vector = transformer.transform(adfa_ld_vector)
    adfa_ld_vector = adfa_ld_vector.toarray()
    predicted = model.predict(adfa_ld_vector)

    app.logger.error(predicted)

    link = url_for('adfaldResult', adfa_ld=adfa_ld, result=predicted[0])
    resp['link'] = str(link)
    return jsonify(resp)

@app.route('/adfa-ld-result')
def adfaldResult():
    req = request.values
    resp_data = {}
    result_id = req['result'] if 'result' in req else ''
    test_api = req['adfa_ld'] if 'adfa_ld' in req else ''
    if not result_id or not test_api:
        return redirect('/')

    resp_data['test_api'] = test_api
    resp_data['result_id'] = int(result_id)

    return render_template('/ADFA-LD/adfa-ld-result.html', **resp_data)




def loadUrlDetect():
    vectorizer = joblib.load('./machine_learning_models/url_detection/vectroizer.pkl')
    model = joblib.load('./machine_learning_models/url_detection/model.pkl')
    return vectorizer, model

def loadDomainModel():
    vectorizer = joblib.load('./machine_learning_models/domain_name/vectroizer.pkl')
    model = joblib.load('./machine_learning_models/domain_name/model.pkl')
    return vectorizer, model

def loadADFALD():
    vectorizer = joblib.load('./machine_learning_models/ADFA-LD/vectroizer.pkl')
    model = joblib.load('./machine_learning_models/ADFA-LD/model.pkl')
    transformer = joblib.load('./machine_learning_models/ADFA-LD/transformer.pkl')
    return vectorizer, model, transformer

if __name__ == '__main__':
    # vectorizer, model = loadUrlDetect()

    app.run(debug=True)

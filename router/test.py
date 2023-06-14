# router/routes.py
from flask import Flask, render_template, jsonify, request
from urllib.parse import unquote
from . import test_app
# 导入其他需要的模块和函数
from service.web import decode_website
from service.summary import summarize_webpage
from service.takumi import takumi_demo,takumi_demo2
from service.ailawyer import LoadPDF_demo,lawyer_demo2
import os


#takumi api test
@test_app.route('/takumi',methods=['POST'])
def get_takumidemo():
    answer = takumi_demo2()
    response = {
        'answer': answer,
    }
    return jsonify(response)


#lawyerai api test
@test_app.route('/lawyer',methods=['POST'])
def get_lawyerdemo():
    request_data = request.json
    question = request_data.get('question')
    answer = lawyer_demo2(question)
    response = {
        'answer': answer,
    }
    return jsonify(response)

#两个测试接口
@test_app.route('/')
def home():
    return render_template('index.html')

@test_app.route('/api/data', methods=['GET','POST'])
def get_data():
    file_path = 'resource/PDF/test.pdf'
    if os.path.isfile(file_path):
        print('File exists.')
    else:
        print('File does not exist.')
    if request.method == 'GET':
        sample_data = {
            'message': 'Hello,API!',
            'data': [1, 2, 3, 4, 5]
        }
        print ("DEBUG",sample_data)
        return jsonify(sample_data)
    elif request.method == 'POST':
        print ("DEBUG request",request)
        encode_url = unquote(unquote(request.args.get('url')))
        print ("DEBUG encode_url",encode_url)
        if not encode_url:
            return jsonify({'error': 'URL is required'}), 400

        decoded_text = decode_website(encode_url)

        print ("DEBUG decoded_text",decoded_text)

        summary = summarize_webpage(decoded_text)

        response = {
            'submitted_url': encode_url,
            'summary': summary,
        }

        return jsonify(response)
        
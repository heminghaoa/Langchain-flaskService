# router/routes.py
from flask import Flask, render_template, jsonify, request
from urllib.parse import unquote
from . import takumi_app
# 导入其他需要的模块和函数
from service.web import decode_website
from service.summary import summarize_webpage
from service.takumi import takumi_demo,takumi_demo2,LoadPDF_demo,takumi_demo3
from service.ailawyer import lawyer_demo2
import os

#takumi api test
@takumi_app.route('/keywordinCSV',methods=['POST'])
def get_takumidemo():
    answer = LoadPDF_demo()
    response = {
        'answer': answer,
    }
    return jsonify(response)


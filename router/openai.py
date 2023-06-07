# router/openai.py
from flask import Flask, jsonify
from . import openai_app


@openai_app.route('/api2', methods=['GET'])
def api2():
    data = {
        'message': 'API 2'
    }
    return jsonify(data)


# router/openai.py
from flask import Flask, jsonify
from . import openai_app
import os
import openai


@openai_app.route('/api2', methods=['GET'])
def api2():
    data = {
        'message': 'API 2'
    }
    return jsonify(data)


@openai_app.route('/chat', methods=['POST'])
def chat():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!what's your name?"}
    ]
    )
    data = {
        'message': completion.choices[0].message
    }
    print(data)
    return jsonify(data)



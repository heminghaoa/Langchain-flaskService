# router/openai.py
from flask import Flask, jsonify,request
from . import openai_app
import os
import openai


@openai_app.route('/api2', methods=['GET'])
def api2():
    data = {
        'message': 'API 2'
    }
    return jsonify(data)


@openai_app.route('/chat', methods=['GET'])
def chat():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    request_data = request.json
    question = request_data.get('question')

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": question}
    ]
    )
    data = {
        'message': completion.choices[0].message
    }
    print(data)
    return jsonify(data)

# {
#   "question": "用日语说你好"
# }

# {
#     "message": {
#         "content": "こんにちは (Konnichiwa)。",
#         "role": "assistant"
#     }
# }



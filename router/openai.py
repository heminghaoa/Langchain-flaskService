# router/openai.py
from flask import Flask, jsonify,request
from . import openai_app
import os
import openai
import json


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

@openai_app.route('/civilTermFinder', methods=['POST'])
def civilTermFinder():
    functions = [{
        "name": "extract_civil_keywords",
        "description": "Extract civil engineering related keywords from a given text",
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The extracted keywords related to civil engineering"
                },

            },
            "required": ["keywords"],
        },

    }]

    openai.api_key = os.getenv("OPENAI_API_KEY")
    request_data = request.json
    description = request_data.get('description')

    try:
        completion = openai.ChatCompletion.create(
            function_call="auto",
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "system",
                    "content": 'You are a helpful assistant.'
                },
                {
                    "role": "user",
                    "content": description
                }
            ],
            functions=functions,
        )
        
        if 'choices' in completion and len(completion['choices']) > 0:
            output_message = completion['choices'][0]['message']['function_call']['arguments']
            return {"keywords": json.loads(output_message) }
        else:
            return jsonify({"error": "No result returned from the model."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)



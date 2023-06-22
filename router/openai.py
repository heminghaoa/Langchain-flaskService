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

    openai.api_key = os.getenv("OPENAI_API_KEY")
    request_data = request.json
    description = request_data.get('description')
    functions = [{
        "name": "extract_civil_keywords",
        "description": f"""
        This is a keyword extraction process that can take a piece of text and extract the most relevant keywords associated with civil and piping engineering. 
        The process should avoid returning non-related words, and only the top five most significant keywords within this field should be returned .
        from {description},
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The keyword is the smallest independent word"

                    },
                    "description": f"""
                           keywords < 6, 
                            """,
                },

            },
            "required": ["keywords"],
        },

    }]



    try:
        completion = openai.ChatCompletion.create(
            function_call="auto",
            temperature=0,
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
            return {"message": json.loads(output_message) }
        else:
            return jsonify({"error": "No result returned from the model."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)



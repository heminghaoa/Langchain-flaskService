# router/openai.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api2', methods=['GET'])
def api2():
    data = {
        'message': 'API 2'
    }
    return jsonify(data)


from flask import Flask

from decouple import config
from router import test_app, openai_app

import os
import nltk
nltk.data.path.append('nltk_data')

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
app = Flask(__name__)

app.register_blueprint(openai_app)

app.register_blueprint(test_app)

#env文件中PORT设置端口号
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)



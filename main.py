from flask import Flask
from flask_cors import CORS
import time

from urls.llm import llm_bp
from urls.customLLM import custom_llm_bp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(llm_bp, url_prefix='/llm')
app.register_blueprint(custom_llm_bp, url_prefix='/custom-llm')

@app.route('/')
def index():
    return {"success": True, "time": int(time.time()*1000)}

if __name__ == "__main__":
    app.run(debug=True)
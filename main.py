from flask import Flask
from flask_cors import CORS
import time
from urls.openai_llm import openai_llm_bp
from urls.pdf_ai_llm import pdf_ai_llm

class Config:
    CORS_HEADERS = 'Content-Type'

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)

# Blueprint for OpenAI LLM endpoints
app.register_blueprint(openai_llm_bp, url_prefix='/openai_llm')

# Blueprint for custom PDF as AI store endpoints
app.register_blueprint(pdf_ai_llm, url_prefix='/pdf_ai_llm')

@app.route('/')
def index():
    """
    Base route to test server status.
    Returns a JSON response with server status and current time.
    """
    return {"success": True, "time": int(time.time()*1000)}

@app.errorhandler(404)
def page_not_found(error):
    return {"error": "Resource not found"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

from app import app



# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'No question provided'}), 400
    if len(question) > 500:
        return jsonify({'error': 'Question is too long. Please keep it under 500 characters.'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant specialized in answering general and technical questions."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=150
        )
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run()

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()

    text = data.get("text")
    language = data.get("language")

    if not text or not language:
        return jsonify({"error": "Missing text or language"}), 400

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate accurately."
                },
                {
                    "role": "user",
                    "content": f"Translate this text to {language}:\n{text}"
                }
            ]
        )

        translated_text = response.output[0].content[0].text

        return jsonify({
            "translated_text": translated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


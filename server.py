from flask import Flask, request, jsonify
import openai
import os, base64

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "پیام خالی ارسال شد"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": user_message}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/image", methods=["POST"])
def image():
    file = request.files.get("image")
    if not file:
        return jsonify({"reply": "فایل تصویری دریافت نشد"}), 400

    image_bytes = file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": f"Describe this image in Persian: {image_b64}"}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

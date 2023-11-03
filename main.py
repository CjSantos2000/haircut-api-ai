import base64
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from haircut import (
    generate_haircut_ai,
)


app = Flask(__name__)
CORS(app)

# Set the maximum file size for uploads to 3MB (3 * 1024 * 1024 bytes)
MAX_CONTENT_LENGTH = 3 * 1024 * 1024


base_url = "https://semaphore.co/api/v4/messages"
api_key = "d976ae4a30b895246d9fc1bc1dabacdb"
allowed_extensions = {"jpg", "jpeg", "png"}


@app.route("/generate-haircut", methods=["POST"])
def ai_generate_haircut():
    if "image" not in request.files:
        return jsonify({"error": "No image part"})

    # Request Payload
    image = request.files["image"]
    haircut = request.form.get("haircut")

    if image.filename == "":
        return jsonify({"error": "No selected file"})

    if (
        "." not in image.filename
        or image.filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        return jsonify({"error": "Invalid file format"})

    # Check if the file size is within the allowed limit
    if len(image.read()) > MAX_CONTENT_LENGTH:
        return jsonify({"error": "File size exceeds the 3MB limit"})

    # Reset the file cursor to read the image content again
    image.seek(0)

    # You can process the image here (optional)
    image_data = generate_haircut_ai(image=image, haircut=haircut)

    # Create a JSON response with the base64-encoded image
    response_data = {
        "image_data": image_data,
        "haircut": haircut,
    }

    return jsonify(response_data)


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image part"})

    # Request Payload
    image = request.files["image"]
    haircut = request.form.get("haircut")

    if image.filename == "":
        return jsonify({"error": "No selected file"})

    if (
        "." not in image.filename
        or image.filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        return jsonify({"error": "Invalid file format"})

    # Check if the file size is within the allowed limit
    if len(image.read()) > MAX_CONTENT_LENGTH:
        return jsonify({"error": "File size exceeds the 3MB limit"})

    # Reset the file cursor to read the image content again
    image.seek(0)

    # You can process the image here (optional)

    # Read the image content and encode it as base64
    image_data = base64.b64encode(image.read()).decode("utf-8")

    # Create a JSON response with the base64-encoded image
    response_data = {
        "haircut": haircut,
        "image_data": "https://img.hair.ailabapi.com/20231103/UnderCut_20231103045909865587_dgwcndcxa48ftj1cy5mq.png",
        "image": str(image),
    }

    return jsonify(response_data)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))

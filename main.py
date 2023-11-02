import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Set the maximum file size for uploads to 3MB (3 * 1024 * 1024 bytes)
MAX_CONTENT_LENGTH = 3 * 1024 * 1024


# Define the route for uploading an image
@app.route("/upload", methods=["POST"])
def upload_image():
    # Check if the 'image' field exists in the request
    if "image" not in request.files:
        return jsonify({"error": "No image part"})

    # Request Payload
    image = request.files["image"]
    haircut = request.form.get("haircut")

    # Check if the file is empty
    if image.filename == "":
        return jsonify({"error": "No selected file"})

    # Check if the file is an allowed format (e.g., you can add more formats)
    allowed_extensions = {"jpg", "jpeg", "png"}
    if (
        "." not in image.filename
        or image.filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        return jsonify({"error": "Invalid file format"})

    # Check if the file size is within the allowed limit
    # if len(image.read()) > app.config["MAX_CONTENT_LENGTH"]:
    if len(image.read()) > MAX_CONTENT_LENGTH:
        return jsonify({"error": "File size exceeds the 3MB limit"})

    # Reset the file cursor to read the image content again
    image.seek(0)

    # You can process the image here (optional)

    # Read the image content and encode it as base64
    image_data = base64.b64encode(image.read()).decode("utf-8")

    # Create a JSON response with the base64-encoded image
    response_data = {
        "filename": image.filename,
        "image_data": image_data,
        "haircut": haircut,
    }

    return jsonify(response_data)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))

import os
from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
from enhancer.api import enhance_image
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://statusdownload8.blogspot.com"}})

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Welcome to the OpenCV Image Enhancer API"

@app.route('/enhance', methods=['POST'])
def enhance():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    # Rename the file if it already exists
    if os.path.exists(input_path):
        new_filename = f"{uuid.uuid4()}_{filename}"
        input_path = os.path.join(UPLOAD_FOLDER, new_filename)

    file.save(input_path)

    # Process the image
    output_filename = f"enhanced_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        enhance_image(input_path, output_path)
        output_url = url_for("static", filename=f"outputs/{output_filename}", _external=True)
        return jsonify({"enhanced_image": output_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
        

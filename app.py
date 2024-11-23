import os
from flask_cors import CORS
from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import logging
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://statusdownload8.blogspot.com"}})

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return "Welcome to the Enhanced Image API!"

@app.route("/enhance", methods=["POST"])
def enhance():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    # Ensure unique filenames for uploads
    if os.path.exists(input_path):
        filename = f"{uuid.uuid4()}_{filename}"
        input_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(input_path)
        output_path = os.path.join(OUTPUT_FOLDER, f"enhanced_{filename}")

        # Enhance the image
        enhance_image(input_path, output_path)

        if not os.path.exists(output_path):
            raise Exception("Enhanced image not created.")

        # Generate URL for the enhanced image
        output_url = url_for("static", filename=f"outputs/enhanced_{filename}", _external=True)
        return jsonify({"enhanced_image": output_url})

    except Exception as e:
        logging.error(f"Error enhancing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    

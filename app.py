from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import os

app = Flask(__name__)

# Define upload and output folder locations
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"  # Update to static/outputs folder


@app.route('/')
def index():
    return "Welcome to the Image Enhancer API"

@app.route("/enhance", methods=["POST"])
def enhance():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    output_path = os.path.join(OUTPUT_FOLDER, f"enhanced_{filename}")
    try:
        enhance_image(input_path, output_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Use static/outputs to get the enhanced image URL
    output_url = url_for("static", filename=f"outputs/enhanced_{filename}", _external=True)
    return jsonify({"enhanced_image": output_url})

if __name__ == "__main__":
    app.run(debug=True)
    

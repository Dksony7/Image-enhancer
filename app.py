from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"  # Update to static/outputs folder

# Ensure the folders exist (if they are not manually created)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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
        # Try enhancing the image
        enhance_image(input_path, output_path)

        # Check if the enhanced image exists
        if not os.path.exists(output_path):
            raise Exception("Enhanced image not created.")
        
        # Generate URL for the enhanced image
        output_url = url_for("static", filename=f"outputs/enhanced_{filename}", _external=True)
        return jsonify({"enhanced_image": output_url})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error to the server logs
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    

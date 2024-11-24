import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from inference_realesrgan import enhance_image
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://statusdownload8.blogspot.com"}})

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to Real-ESRGAN API"

@app.route('/enhance', methods=['POST'])
def enhance():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    output_filename = f"enhanced_{uuid.uuid4().hex}.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        # Enhance the image
        enhance_image(input_path, output_path)

        # Return the result
        output_url = url_for("static", filename=f"outputs/{output_filename}", _external=True)
        return jsonify({"enhanced_image": output_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os

    # Get the port from environment variables or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Ensure the app runs on the correct host and port
    app.run(host="0.0.0.0", port=port, debug=True)

    

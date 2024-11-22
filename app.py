from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

    output_url = url_for("static", filename=f"outputs/enhanced_{filename}", _external=True)
    return jsonify({"enhanced_image": output_url})

if __name__ == "__main__":
    app.run(debug=True)
    

from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import os

app = Flask(__name__, static_folder="static")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"  # Ensure this is inside the static folder


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
        print(f"Enhanced image saved at {output_path}")  # Log for debugging
    except Exception as e:
        return jsonify({"error": f"Enhance function failed: {str(e)}"}), 500

    # Ensure output image exists
    if not os.path.exists(output_path):
        return jsonify({"error": "Enhanced image not created"}), 500

    # Generate the URL to the enhanced image
    output_url = url_for("static", filename=f"outputs/enhanced_{filename}", _external=True)
    return jsonify({"enhanced_image_url": output_url})

if __name__ == "__main__":
    app.run(debug=True)
    

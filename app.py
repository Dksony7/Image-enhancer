from flask import Flask, request, jsonify
from enhancer.api import enhance_image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/enhance", methods=["POST"])
def enhance():
    """
    API endpoint to enhance an uploaded image.
    Returns the path to the enhanced image.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Enhance the image
    output_path = os.path.join(OUTPUT_FOLDER, f"enhanced_{file.filename}")
    try:
        enhance_image(input_path, output_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"enhanced_image": output_path})

if __name__ == "__main__":
    app.run(debug=True)
    

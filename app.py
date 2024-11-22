from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from enhancer.api import enhance_image
import os

app = Flask(__name__)

# Define directories
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static/outputs"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route("/enhance", methods=["POST"])
def enhance():
    """
    API endpoint to enhance an uploaded image.
    """
    # Check if file is in the request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    # Define output path
    output_filename = f"enhanced_{filename}"
    output_path = os.path.join(STATIC_FOLDER, output_filename)

    try:
        # Enhance the image
        enhance_image(input_path, output_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Return the static URL for the enhanced image
    output_url = url_for("static", filename=f"outputs/{output_filename}", _external=True)
    return jsonify({"enhanced_image_url": output_url})

if __name__ == "__main__":
    app.run(debug=True)
    

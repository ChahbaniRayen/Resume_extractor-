import spacy
from extractor import ResumeExtractor
from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
import os

# Load the spaCy model

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/extract_resume", methods=["POST"])
def extract_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Extract text from PDF
        text = extract_text(filepath)

        # Use ResumeExtractor to extract information
        extractor = ResumeExtractor(nlp)
        info = extractor.extract(text)

        # Clean up the uploaded file
        os.remove(filepath)

        return jsonify(info)

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)

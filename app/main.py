from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from app.services.firecrawl import parse_pdf
from app.services.mistral import summarize_text

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app = Flask(__name__, static_folder="../static", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE  # Flask-level hard cap
CORS(app)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/summarize", methods=["POST"])
def summarize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    user_prompt = request.form.get("prompt", "Summarize the key points.")

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        file_bytes = file.read()

        if len(file_bytes) > MAX_FILE_SIZE:
            return jsonify({"error": "File exceeds 5MB limit"}), 413

        parsed_text, metadata = parse_pdf(file_bytes, file.filename)
        summary = summarize_text(parsed_text, user_prompt)

        response = {
            "filename": file.filename,
            "prompt": user_prompt,
            "summary": summary,
            "pagesParsed": metadata.get("numPages"),
            "totalPages": metadata.get("totalPages"),
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File exceeds 5MB limit"}), 413


if __name__ == "__main__":
    app.run(debug=True, port=5000)

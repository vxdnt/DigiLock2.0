from flask import Flask, render_template, redirect, url_for, request
from passport_aadhaar_pan import detect
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_file"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload_file", methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file_input"]
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # detecting pii using ML
        message_detection, message_status = detect(file_path)
        message = f"{message_detection}, {message_status}"
        if message_status:
            return render_template("submit.html", message_detection=message_detection, message_status=True, message=message)
        else:
            return render_template("submit.html", message_detection=message_detection, message_status=False, message=message)
    return render_template("input_files.html")
@app.route('/docs')
def data():
    return render_template('docs.html')

if __name__ == "__main__":
    app.run(debug =True)
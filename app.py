# Patched Version

from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import random
import string
import time
import re
import imghdr

clean = time.time()
chars = list(string.ascii_letters + string.digits)

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 24 * 1000 * 1000

@app.route('/')
def main():
    return open("index.html").read()

@app.route('/generate', methods=['POST'])
def generate():
    global clean
    if time.time() - clean > 60:
      os.system("rm static/images/*")
      clean = time.time()
    text = request.form.getlist('text')[0]
    text = text.replace("\"", "")
    # Character Whitelisting
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    filename = "".join(random.choices(chars,k=8)) + ".png"
    os.system(f"python3 generate.py {filename} \"{text}\"")
    return redirect(url_for('static', filename='images/' + filename), code=301)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return (format if format != 'jpeg' else 'jpg')

@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()

    # Extension Whitelisting + Magic Header Validation
    if file and allowed_file(file.filename) and file_ext == validate_image(file.stream):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('static', filename='uploads/' + filename), code=301)
    else:
        return open("restricted.html").read()

def is_safe_path(basedir, path):
    # Pathname Canonicalization
    matchpath = os.path.realpath(path)
    return basedir == os.path.commonpath((basedir, matchpath))

@app.route("/download")
def download():
    filename = request.args.get("file")
    if is_safe_path(os.getcwd(), filename):
        return send_file(filename)
    else:
        return open("error.html").read()

if __name__ == '__main__':
    app.run()
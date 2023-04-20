from flask import Flask, request, redirect, url_for, send_file
import os
import random
import string
import time

clean = time.time()
chars = list(string.ascii_letters + string.digits)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    filename = "".join(random.choices(chars,k=8)) + ".png"
    os.system(f"python3 generate.py {filename} \"{text}\"")
    return redirect(url_for('static', filename='images/' + filename), code=301)

@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file = request.files["file"]
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(filename)

if __name__ == '__main__':
    app.run()

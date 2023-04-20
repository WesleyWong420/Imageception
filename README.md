# Imageception
Flask Powered Vulnerable Image Generator

## Installation
```
git clone https://github.com/WesleyWong420/Imageception.git
cd Imageception/
chmod +x build.sh
./build.sh
curl http://localhost:1005
```
## Potential Vulnerabilities
| Vulnerability            | Mitigation Measure         | Common Weakness Enumeration (CWE) |
|:------------------------:|:--------------------------:|:---------------------------------:|
| OS Command Injection     | Input Sanitization         | CWE-20, CWE-74, CWE-78            |
| Directory Trasversal     | Pathname Canonicalization  | CWE-20, CWE-22                    |
| Unrestricted File Upload | File Attributes Validation | CWE-434                           |

## Vulnerability Exploitation
### OS Command Injection
User input is received from the client-side without enforcing proper input validation. Unsanitized user input is passed downstream to the generator component and used directly as a parameter for *os.system()*. The *os.system()* function is used by Imageception to invoke *generate.py* as a way to implement image generation.

```
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
```

[[Payload]](./resources/OS-Command-Injection-1.png)
[[Result]](./resources/OS-Command-Injection-2.png)

### Directory Traversal
The *file* parameter (unvalidated path) in the query string of the UR  is used directly in *send_file()* to return the specified file without any proper validation or sanitization.

```
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(filename)
```

[[Payload]](./resources/Directory-Traversal-1.png)
[[Result]](./resources/Directory-Traversal-2.png)

### Unrestricted File Upload
The system does not implement any form of validation checks to ensure the integrity and safety of the uploaded file before saving it to the destination folder. The uploaded file is saved directly upon receiving the file from upstream. 

In addition to that, the use of *os.path.join()* function also introduces Directory Traversal vulnerability when constructing the file path for saving the uploaded file. The combination of these 2 vulnerabilities allows an attacker to upload malicious files to any arbitrary location.

```
@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file = request.files["file"]
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
```

[[Uploading Python File]](./resources/Unrestricted-File-Upload-1.png)
[[Content of Python Script]](./resources/Unrestricted-File-Upload-2.png)
[[Manipulate Upload Desination]](./resources/Unrestricted-File-Upload-3.png)
[[Result]](./resources/Unrestricted-File-Upload-4.png)

## Secure Coding Concepts
### Restriction of Special Characters (Input Sanitization)
User input is first validated against a set of whitelisted characters. Any characters from the input field that does not belong to either of the regular expression set [a-z], [A-Z] and [0-9] are discarded before passing to the *os.system()* function.

```
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
```

### Pathname Canonicalization
First, the base directory of upload folder /app/static/uploads is retrieved using the function *os.getcwd()*. The canonicalized path of the requested resource is then determined using the *realpath()* function. The resulting canonicalized path is validated to check if it starts with the base directory. If it does, access to the file is permitted. Otherwise, the user will be redirected to an error page. This is to ensure that users can only access files within the intended area of the file system.

```
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
```

### Extension Whitelisting & Magic Header Validation (File Attributes Validation)
- Define a whitelist of allowed file extensions.
- Specify the maximum file size of 24MB.
- Extract the header signature of the file stream.

```
app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 24 * 1000 * 1000

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
```

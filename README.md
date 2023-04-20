# Imageception
Flask Powered Vulnerable Image Generator

![](./resources/Main-1.png)

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
**CAPEC-88: OS Command Injection**

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
**CAPEC-126: Path Traversal**

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
**CAPEC-17: Using Malicious Files**

The system does not implement any form of validation checks to ensure the integrity and safety of the uploaded file before saving it to the destination folder. The uploaded file is saved directly upon receiving the file from upstream. In addition to that, the use of os.path.join() function also introduces Directory Traversal vulnerability when constructing the file path for saving the uploaded file. The combination of these 2 vulnerabilities allows an attacker to upload malicious files to any arbitrary location.

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

[Uploading Python File](./resources/Unrestricted-File-Upload-1.png)
[Content of Python Script](./resources/Unrestricted-File-Upload-2.png)
[Manipulate Upload Desination](./resources/Unrestricted-File-Upload-3.png)
[Result](./resources/Unrestricted-File-Upload-4.png)

## Secure Coding Concepts

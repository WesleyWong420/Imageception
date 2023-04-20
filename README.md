# Imageception
Flask Powered Vulnerable Image Generator

![](./resources/Main-1.png)
![](./resources/Main-2.png)

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
User input is received from the client-side without enforcing proper input validation. Unsanitized user input is passed downstream to the generator component and used directly as a parameter for os.system() in Line 27. The os.system() function is used by Imageception to invoke generate.py as a way to implement image generation.

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

[Payload](./resources/OS-Command-Injection-1.png)
[Result](./resources/OS-Command-Injection-2.png)

### Directory Traversal
![](./resources/Directory-Traversal-1.png)
![](./resources/Directory-Traversal-2.png)

### Unrestricted File Upload
![](./resources/Unrestricted-File-Upload-1.png)
![](./resources/Unrestricted-File-Upload-2.png)
![](./resources/Unrestricted-File-Upload-3.png)
![](./resources/Unrestricted-File-Upload-4.png)

## Secure Coding Concepts

# Imageception
Flask Powered Vulnerable Image Generator

## Features
### Generate Text-Embedded Image
![](./resources/Main-1.png)

### Change Base Image
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
![](./resources/OS-Command-Injection-1.png)
![](./resources/OS-Command-Injection-2.png)

### Directory Traversal
![](./resources/Directory-Traversal-1.png)
![](./resources/Directory-Traversal-2.png)

### Unrestricted File Upload
![](./resources/Unrestricted-File-Upload-1.png)
![](./resources/Unrestricted-File-Upload-2.png)
![](./resources/Unrestricted-File-Upload-3.png)
![](./resources/Unrestricted-File-Upload-4.png)

## Secure Coding Concepts

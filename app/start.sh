#!/bin/sh
chmod 777 /app/static/images
chmod 7777 /app/uploads
gunicorn --chdir /app app:app -w 4 --threads 4 -b 0.0.0.0:1337

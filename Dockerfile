FROM python:3-alpine

RUN pip install --no-cache-dir flask gunicorn
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache g++ freetype-dev jpeg-dev zlib-dev
RUN pip install Pillow
RUN apk del .tmp

RUN addgroup -S ctf && adduser -S ctf -G ctf

COPY app /app
WORKDIR /app

RUN chown -R ctf:ctf /app && chmod -R 770 /app
RUN chown -R root:ctf /app && \
  chmod -R 770 /app
RUN chmod -R 777 /app/static/images
RUN chmod -R 777 /app/static/uploads

USER ctf
ENTRYPOINT ["/app/start.sh"]

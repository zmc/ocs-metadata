FROM python:3.7-alpine
COPY requirements.txt main.py settings.py scrape.py /data/
RUN \
  pip3 --no-cache-dir install -r /data/requirements.txt
EXPOSE 5000
WORKDIR /data
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "gunicorn --bind 0.0.0.0:5000 main:app"]

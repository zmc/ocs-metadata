#FROM fedora:30
FROM python:3.7-alpine
RUN \
  mkdir /data && \
  pip3 --no-cache-dir install eve gunicorn
COPY main.py settings.py /data/
EXPOSE 5000
WORKDIR /data
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "gunicorn --bind 0.0.0.0:5000 main:app"]

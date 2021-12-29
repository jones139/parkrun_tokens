FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update && apt-get install  gcc
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./ /app
RUN pip install -r /app/requirements.txt


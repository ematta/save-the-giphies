FROM python:3.8
LABEL maintainer="Enrique Matta <enrique@matta.dev>"
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN pip install uwsgi
CMD [ "uwsgi", "app.ini" ]
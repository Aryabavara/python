FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN apk add mysql-client gcc
RUN apk add mariadb-connector-c-dev
RUN pip install -r requirements.txt
RUN pip install mysqlclient
COPY app.py .
#CMD ["python", "./app.py"]
ENV FLASK_APP="app.py"
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
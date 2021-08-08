FROM python:3.8.11-alpine3.14
RUN apk update && apk add --no-cache npm jpeg-dev \
        zlib-dev postgresql-dev gcc python3-dev musl-dev
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN npm install
RUN python3.8 -m pip install -U --force-reinstall pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary==2.8.6
EXPOSE 8000
RUN python manage.py migrate
RUN python manage.py collectstatic
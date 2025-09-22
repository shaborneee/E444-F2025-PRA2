FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

ENV FLASK_APP=hello.py

CMD [ "flask", "run", "--host=0.0.0.0"]

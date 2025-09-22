FROM python:3.6-alpine

ENV FLASK_APP flasky.py
ENV FLASK_ENV=production

WORKDIR /home/flasky

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY ..

EXPOSE 5000

# Run the Flask app
CMD ["python", "flasky.py"]

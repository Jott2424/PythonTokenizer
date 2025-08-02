FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /logs && chown -R 1000:1000 /logs

EXPOSE 5000

CMD ["python", "app.py"]
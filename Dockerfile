FROM python:3.13-slim

WORKDIR /app

EXPOSE 5000

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "--app", "server", "run", "--host=0.0.0.0", "--port=5000"]


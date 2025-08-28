FROM python:3.11-slim

WORKDIR /app

RUN pwd

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app
COPY ./src /app/

CMD ["python", "src/main.py"]
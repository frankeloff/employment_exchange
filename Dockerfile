FROM python:3.10-slim

WORKDIR /src

COPY ./app ./app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]

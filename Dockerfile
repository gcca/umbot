FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/venv/bin/sanic", "umbot", "-H0.0.0.0", "-p8000"]

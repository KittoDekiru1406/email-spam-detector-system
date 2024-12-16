FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./data /app/
COPY ./frontend /app/
COPY ./src /app/
COPY ./weights /app/
COPY app.py /app/
COPY entrypoint.sh /app/
COPY utils.py /app/

CMD ["sh", "entrypoint.sh"]
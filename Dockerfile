FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY data /app/data
COPY frontend /app/frontend
COPY src /app/src
COPY weights /app/weights
COPY app.py /app/
COPY entrypoint.sh /app/
COPY utils.py /app/

# Thêm thư mục gốc vào PYTHONPATH
ENV PYTHONPATH=/app

CMD ["sh", "entrypoint.sh"]
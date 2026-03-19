FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV HOSTNAME='0.0.0.0' \
    PORT=9804 \
    MODEL='gpt-4o-mini'

EXPOSE 9804
CMD ["python3", "main.py"]

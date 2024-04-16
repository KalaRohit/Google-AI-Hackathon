FROM python:3.11.9-slim

WORKDIR /app

COPY Backend/ /app/

RUN pip install --no-cache-dir  -r requirements.txt
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD uvicorn simple_script_server:app --port 8000 --host 0.0.0.0
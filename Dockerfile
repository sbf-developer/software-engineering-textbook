FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY examples/python /app/examples/python
EXPOSE 8000
USER nobody
CMD ["python", "examples/python/app.py"]


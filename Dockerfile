FROM python:3.11-slim

RUN mkdir /app
WORKDIR /app

RUN pip install --no-cache-dir --upgrade fastapi[all] prisma

COPY ./app /app

CMD ["uvicorn", "main:app", "--reload", "--host","0.0.0.0","--port","8000"]

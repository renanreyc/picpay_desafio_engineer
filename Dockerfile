FROM python:3.12-slim

WORKDIR /app

COPY /src .
COPY requirements.txt .
COPY requirements-dev.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

EXPOSE 5000

CMD ["fastapi dev", "src.app"]
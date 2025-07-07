FROM python:3.13.3-alpine

RUN apk update && \
    apk add --no-cache ffmpeg

WORKDIR /app

COPY requirements.txt .

# Só instala dependências se o arquivo existir
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/__main__.py"]


FROM python:3.13.3-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    sqlite \
    build-base



WORKDIR /app

COPY requirements.txt .

# Só instala dependências se o arquivo existir
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src"]

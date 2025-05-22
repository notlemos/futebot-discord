FROM python:3.13.3-alpine

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean



WORKDIR /app

COPY requirements.txt .

# Só instala dependências se o arquivo existir
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src"]

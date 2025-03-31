FROM python:3.12.2

RUN apt-get update && apt-get install -y sqlite3

WORKDIR /app

COPY requirements.txt .

# Só instala dependências se o arquivo existir
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
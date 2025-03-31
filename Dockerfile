FROM python:3.12.2

RUN apt-get update && apt-get install -y sqlite3

WORKDIR /app

COPY requirements.txt .

# Só instala dependências se o arquivo existir
<<<<<<< HEAD
RUN pip install -r requirements.txt; pip install --upgrade pip
=======
RUN pip install -r requirements.txt
>>>>>>> f92e80997252bd39e5e5c27a54c0248a59ad0354

COPY . .

CMD ["python", "main.py"]
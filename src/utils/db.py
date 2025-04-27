import sqlite3
from pathlib import Path

DB_PATH = Path("/app/data/database.sqlite")  # Caminho absoluto no contêiner

class DBManager:
    def __init__(self):
        self._create_table()

    def _connect(self):
        try:
            return sqlite3.connect(DB_PATH)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS filmes (
                    id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    filme TEXT, 
                    nota1 FLOAT, 
                    nota2 FLOAT
                )
                '''
            )
            conn.commit()

    def save_movie(self, name: str, filme: str, nota1: float, nota2: float):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO filmes (name, filme, nota1, nota2)
                VALUES (?, ?, ?, ?)
            ''', (name, filme, nota1, nota2))
            conn.commit()

    def delete_movie(self, movie_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM filmes WHERE id = ?", (movie_id,))
            conn.commit()
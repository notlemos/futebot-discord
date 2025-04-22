import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "app/data/database.sqlite"

class DBManager:
    def __init__(self):
        self._create_table()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

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
            cursor = conn.cursor()  # Corrigido: usei os parênteses
            cursor.execute('''INSERT INTO filmes (name, filme, nota1, nota2)
                VALUES (?, ?, ?, ?)
            ''', (name, filme, nota1, nota2))
            conn.commit()

    def delete_movie(self, movie_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM filmes WHERE id = ?", (movie_id,))  # Corrigido: adicionei vírgula
            cursor.execute("""
                CREATE TEMP TABLE temp_filmes AS 
                SELECT ROW_NUMBER() OVER () AS new_id, name, filme, nota1, nota2 
                FROM filmes ORDER BY id ASC;
            """)
            cursor.execute("DELETE FROM filmes")
            cursor.execute("""
                INSERT INTO filmes (id, name, filme, nota1, nota2)
                SELECT new_id, name, filme, nota1, nota2 FROM temp_filmes;
            """)
            conn.commit()
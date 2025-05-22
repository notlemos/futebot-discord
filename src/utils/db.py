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
class DBFute:
    def __init__(self):
        self._create_table()
    def _connect(self):
        try:
            return sqlite3.connect("src/data/brasileirao.db")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
    def _create_table(self):
         with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jogos(
                    rodada INTEGER,
                    id_jogo INTEGER,
                    mandante TEXT,
                    visitante TEXT,
                    gols_mandante INTEGER,
                    gols_visitante INTEGER,
                    data TEXT
                )
            ''')
            conn.commit()
    def inserir_jogos_at(self, gols_mandante: int, gols_visitante: int, rodada: int, id_jogo: int):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                    UPDATE jogos 
                    SET gols_mandante = ?, gols_visitante = ?
                    WHERE rodada = ? AND id_jogo = ?
                    
                           ''', (
                    gols_mandante,
                    gols_visitante,
                    rodada,
                    id_jogo
            ))
    def inserir_jogos(self, jogos):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            for jogo in jogos:
                cursor.execute('''
                    INSERT OR REPLACE INTO jogos
                    (rodada, id_jogo, mandante, visitante, gols_mandante, gols_visitante, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    jogo['Rodada'],
                    jogo['id_jogo'],
                    jogo['Mandante'],
                    jogo['Visitante'],
                    jogo['Gols Mandante'],
                    jogo['Gols Visitante'],
                    jogo['Data']
                ))
    def get_jogo_by_rodada(rodada):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jogos WHERE rodada = ?", (rodada,))
            resultado = cursor.fetchall
            return resultado
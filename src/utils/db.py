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
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS jogos(
                    rodada INTEGER,
                    id_jogo INTEGER,
                    sigla_mandante TEXT,
                    mandante TEXT,
                    sigla_visitante TEXT,
                    visitante TEXT,
                    gols_mandante INTEGER,
                    gols_visitante INTEGER,
                    data TEXT
                )
            ''')
            conn.commit()
    

            
    def getAcronym(self, time):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sigla_mandante FROM jogos 
                           WHERE mandante = ? 
            ''', (time,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        

    def inserir_jogos(self, jogos):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            for jogo in jogos:
                cursor.execute("""
                    SELECT 1 FROM jogos
                    WHERE rodada = ? AND mandante = ? AND visitante = ?
                """, (jogo['Rodada'], jogo['Mandante'], jogo['Visitante']))
                
                if cursor.fetchone():
                    cursor.execute('''
                        UPDATE jogos SET
                            id_jogo = ?, gols_mandante = ?, gols_visitante = ?, data = ?
                        WHERE rodada = ? AND mandante = ? AND visitante = ?
                    ''', (
                        jogo['id_jogo'],
                        jogo['Gols Mandante'],
                        jogo['Gols Visitante'],
                        jogo['Data'],
                        jogo['Rodada'],
                        jogo['Mandante'],
                        jogo['Visitante']
                    ))
                else:
                    cursor.execute('''
                        INSERT INTO jogos
                        (rodada, id_jogo, sigla_mandante, mandante, sigla_visitante, visitante, gols_mandante, gols_visitante, data)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        jogo['Rodada'],
                        jogo['id_jogo'],
                        jogo['Sigla Mandante'],
                        jogo['Mandante'],
                        jogo['Sigla Visitante'],
                        jogo['Visitante'],
                        jogo['Gols Mandante'],
                        jogo['Gols Visitante'],
                        jogo['Data']
                    ))
            conn.commit()
    def get_jogo_by_rodada(self,rodada):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jogos WHERE rodada = ?", (rodada,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
        
    def get_jogos(self, data_inicio, data_fim):
         with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jogos WHERE strftime('%m-%d', data)  BETWEEN ? AND ?", 
            (data_inicio, data_fim,))
            resultado = cursor.fetchall()
            return resultado
         
    def get_next_empty_round(self):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
        cursor.execute('''SELECT rodada FROM jogos WHERE gols_mandante = '' AND gols_visitante = '' LIMIT 1 ''') 
        resultado = cursor.fetchone()
        return resultado
    
    def get_next_round(self):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
        cursor.execute('''SELECT rodada FROM jogos WHERE gols_mandante != '' AND gols_visitante != '' ORDER BY rodada DESC LIMIT 1 ''') 
        resultado = cursor.fetchone()
        return resultado[0]
    
    def get_gols(self):
        with sqlite3.connect("src/data/brasileirao.db") as conn:
            cursor = conn.cursor()
        cursor.execute('''SELECT mandante, visitante, gols_mandante, gols_visitante FROM jogos WHERE gols_mandante != '' AND gols_visitante != '' ''')
        resultado = cursor.fetchall()
        return resultado




class DBTabela:
    def __init__(self):
        ...
        
    def _connect(self):
        conn = sqlite3.connect("src/data/tabela_brasileirao.db")
        conn.row_factory = sqlite3.Row
        return conn

    

    def _create_table(self, user):
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'''
                    CREATE TABLE IF NOT EXISTS tabela_{user} (
                        posicao INTEGER,
                        name TEXT PRIMARY KEY,
                        acronym TEXT,
                        pontos INTEGER,
                        rodada INTEGER
                    )
                    '''
                )
                conn.commit()
    def inserir_times(self, time, acronym, pontos, posicao, rodada, user):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'''
                INSERT OR REPLACE INTO tabela_{user}
                (name, acronym, pontos, posicao, rodada)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (time, acronym, pontos, posicao, rodada)
            )
            conn.commit()

    def get_tabela(self, user):
        table_name = f"tabela_{user}"
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )

            if cursor.fetchone() is None:
                return None

            cursor.execute(
                f'''
                SELECT name, pontos, acronym, rodada FROM tabela_{user}
            '''
            )
            result = cursor.fetchall()
            return [dict(row) for row in result]

    def excluir_table(self, user):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'''DROP TABLE tabela_{user}'''
            )

    def atualizar_pontos(self, time, case, user):
        with self._connect() as conn:
            cursor = conn.cursor()

            if case == 'V':
                cursor.execute(
                    f'''
                        UPDATE tabela_{user}
                        SET pontos = pontos + 3
                        WHERE name = ?
                    ''', (time,)
                )

            elif case == 'E':
                if isinstance(time, (list, tuple)):
                    for t in time:
                        cursor.execute(
                            f'''
                            UPDATE tabela_{user}
                            SET pontos = pontos + 1
                            WHERE name = ?
                            ''', (t,)
                        )
            conn.commit()

    def incrementar_rodada(self, user):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'''
                UPDATE tabela_{user}
                SET rodada = rodada + 1
                '''
            )
            conn.commit()
    def get_rodada(self, user):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'''SELECT rodada from tabela_{user}''')
        response = cursor.fetchone()
        return response

    def reorder_positions(self, user):
        with self._connect() as conn:
            cursor = conn.cursor()
            
            cursor.execute(f'''
                SELECT name, acronym, pontos, rodada FROM tabela_{user}
                ORDER BY pontos DESC, name ASC
            ''')
            ordenados = cursor.fetchall()


            cursor.execute(f"DELETE FROM tabela_{user}")
            
            for posicao, (name, acronym, pontos, rodada) in enumerate(ordenados, start=1):
                cursor.execute(f'''
                    INSERT INTO tabela_{user} (posicao, name, acronym, pontos, rodada)
                    VALUES (?, ?, ?, ?, ?)
                ''', (posicao, name, acronym, pontos, rodada))

            conn.commit()
class DBUsers:
    @staticmethod
    def create(id):
        with sqlite3.connect("src/data/users.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                CREATE TABLE IF NOT EXISTS users_{id} (
                    discordId TEXT PRIMARY KEY,
                    letterboxdUser TEXT NOT NULL
                )
            ''')
    @staticmethod
    def replace(id, discordid, user):
        with sqlite3.connect("src/data/users.db") as conn:
            c = conn.cursor()
            c.execute(
                f'REPLACE INTO users_{id} (discordId, letterboxdUser) VALUES (?, ?)',
                (discordid, user)
            )
    @staticmethod
    def select(id, discordid):
        with sqlite3.connect("src/data/users.db") as conn:
            c = conn.cursor()
            c.execute(
                f'SELECT letterboxdUser FROM users_{id} WHERE discordId = ?',
                (discordid,)
            )
            result = c.fetchone()
        return result[0] if result else None
    @staticmethod
    def selectOneRandom(id):
        with sqlite3.connect("src/data/users.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                SELECT letterboxdUser FROM users_{id} ORDER BY RANDOM() LIMIT 1
            ''')
            return c.fetchone()
class DBRank:
    @staticmethod
    def create(id):
        with sqlite3.connect("src/data/rankUsers.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                CREATE TABLE IF NOT EXISTS rank_{id} (
                    discord_id TEXT PRIMARY KEY,
                    discord_user TEXT NOT NULL,
                    score INTEGER DEFAULT 0
                )
            ''')
    @staticmethod 
    def addPerson(id, discord_id, discord_user):
         with sqlite3.connect("src/data/rankUsers.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                INSERT INTO rank_{id} (discord_id, discord_user) VALUES (?, ?)
            ''', (discord_id, discord_user))
    @staticmethod
    def incrementScore(id, discord_id):
        with sqlite3.connect("src/data/rankUsers.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                UPDATE rank_{id}
                SET score = score + 1 
                where discord_id = ?
                
        ''', (discord_id,))
    @staticmethod
    def getUserById(id, discord_id):
        with sqlite3.connect("src/data/rankUsers.db") as conn:
            c = conn.cursor()
            c.execute(f'''
            SELECT discord_user FROM rank_{id} WHERE discord_id = ?
            ''', (discord_id,))
            result = c.fetchone()
            return result is not None
    @staticmethod 
    def getRankOrder(id):
        with sqlite3.connect("src/data/rankUsers.db") as conn:
            c = conn.cursor()
            c.execute(f'''
                SELECT discord_user, score, discord_id FROM rank_{id} ORDER BY score DESC
            ''')
            return c.fetchall()
    
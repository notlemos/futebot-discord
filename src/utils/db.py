import sqlite3
from pathlib import Path


DB_PATH = Path("/app/data/database.sqlite")  # Caminho absoluto no contêiner
class DBSimulateTable:
    @staticmethod
    def connect():
        return sqlite3.connect('src/data/simulations.db')
    @staticmethod
    def setup():
        with DBSimulateTable.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulation_positions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                team TEXT NOT NULL,
                FOREIGN KEY (simulation_id) REFERENCES simulations(id),
                UNIQUE (simulation_id, position),
                UNIQUE (simulation_id, team)
            )    
            """)
            conn.commit()
    @staticmethod
    def getOrCreateSimulation(user_id: int) -> int:
        with DBSimulateTable.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM simulations WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row: 
                return row[0]
            cursor.execute(
                "INSERT INTO simulations (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return cursor.lastrowid
    @staticmethod
    def savePosition(simulation_id: int, position: int, team: str):
        with DBSimulateTable.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO simulation_positions
                (simulation_id, position, team)
                VALUES (?, ?, ?)
            """, (simulation_id, position, team))
    @staticmethod
    def getPositions(simulation_id: int):
        with DBSimulateTable.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT position, team
                FROM simulation_positions
                WHERE simulation_id = ?
                ORDER BY position ASC
            """, (simulation_id,))
            return cursor.fetchall()
    @staticmethod
    def deleteSimuletion(simulation_id: int):
        with DBSimulateTable.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM simulation_positions WHERE simulation_id = ?", (simulation_id,))  
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
    
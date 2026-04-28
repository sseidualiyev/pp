import psycopg2

DB_CONFIG = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    conn.close()

def get_or_create_player(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    player_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return player_id

def save_session(player_id, score, level):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    conn.close()

def get_leaderboard():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10;
    """)

    data = cur.fetchall()
    conn.close()
    return data

def get_best_score(player_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score) FROM game_sessions WHERE player_id=%s
    """, (player_id,))

    best = cur.fetchone()[0]
    conn.close()
    return best or 0
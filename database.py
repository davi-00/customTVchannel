import sqlite3
import os
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS episodes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            series      TEXT NOT NULL,
            season      INTEGER NOT NULL,
            episode     INTEGER NOT NULL,
            title       TEXT,
            filepath    TEXT NOT NULL UNIQUE,
            added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS watches (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id      INTEGER NOT NULL,
            watched_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            stopped_at_sec  INTEGER DEFAULT 0,
            completed       INTEGER DEFAULT 0,
            FOREIGN KEY (episode_id) REFERENCES episodes(id)
        );

        CREATE TABLE IF NOT EXISTS themes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            label       TEXT NOT NULL,
            color_hex   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS episode_themes (
            episode_id  INTEGER NOT NULL,
            theme_id    INTEGER NOT NULL,
            PRIMARY KEY (episode_id, theme_id),
            FOREIGN KEY (episode_id) REFERENCES episodes(id),
            FOREIGN KEY (theme_id)  REFERENCES themes(id)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database inizializzato in: {DB_PATH}")
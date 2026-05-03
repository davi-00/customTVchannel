import os
import re
from database import get_connection
from config import LIBRARY_PATHS, SUPPORTED_EXTENSIONS


FILENAME_PATTERN = re.compile(
    r"S(?P<season>\d{2})E(?P<episode>\d{2})\s*-\s*(?P<title>.+?)\s*-\s*\[",
    re.IGNORECASE
)


def parse_filename(filename):
    match = FILENAME_PATTERN.search(filename)
    if not match:
        return None
    return {
        "season":  int(match.group("season")),
        "episode": int(match.group("episode")),
        "title":   match.group("title").strip(),
    }


def scan_library():
    conn = get_connection()
    cursor = conn.cursor()
    added = 0
    skipped = 0

    for series_key, library_path in LIBRARY_PATHS.items():
        if not os.path.exists(library_path):
            print(f"[WARN] Percorso non trovato: {library_path}")
            continue

        for root, dirs, files in os.walk(library_path):
            dirs.sort()
            for filename in sorted(files):
                ext = os.path.splitext(filename)[1].lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    continue

                parsed = parse_filename(filename)
                if not parsed:
                    print(f"[SKIP] Nome non riconosciuto: {filename}")
                    skipped += 1
                    continue

                filepath = os.path.join(root, filename)

                cursor.execute(
                    "SELECT id FROM episodes WHERE filepath = ?",
                    (filepath,)
                )
                if cursor.fetchone():
                    skipped += 1
                    continue

                cursor.execute("""
                    INSERT INTO episodes (series, season, episode, title, filepath)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    series_key,
                    parsed["season"],
                    parsed["episode"],
                    parsed["title"],
                    filepath,
                ))
                added += 1

    conn.commit()
    conn.close()
    print(f"[SCAN] Completato — aggiunti: {added}, saltati: {skipped}")

#
if __name__ == "__main__":
    from database import init_db
    init_db()
    scan_library()
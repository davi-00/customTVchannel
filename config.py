import os

# Percorsi libreria video
LIBRARY_PATHS = {
    "the_simpsons": r"C:\Users\davip\Downloads\The Simpsons",
}

# Percorso database
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "casualtv.db")

# Percorso themes
THEMES_PATH = os.path.join(os.path.dirname(__file__), "data", "themes.json")

# Estensioni video supportate
SUPPORTED_EXTENSIONS = [".mkv", ".mp4", ".avi"]

# Porta server
PORT = 5000

# Quanti secondi tra un salvataggio automatico del timestamp
AUTOSAVE_INTERVAL_SEC = 30
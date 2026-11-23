import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "mock").lower()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

if MODE not in ["mock", "real"]:
    raise ValueError("MODE doit être mock ou real")

if MODE == "real" and not GROQ_API_KEY:
    raise ValueError("La clé API Groq est manquante dans le fichier .env")
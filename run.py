"""Entry point for production - run via: python run.py
Forces APP_ENV=production and FLASK_DEBUG=false."""
import os
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("APP_ENV", "production")
os.environ.setdefault("FLASK_DEBUG", "false")

from app import create_app
from waitress import serve
from config import Config

app = create_app()
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 5000))
print(f"[SARA] Environment: {Config.APP_ENV}")
print(f"[SARA] Debug mode: {Config.DEBUG}")
print(f"[SARA] Running on http://{host}:{port}")
serve(app, host=host, port=port, threads=8)

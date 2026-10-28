import os
from dotenv import load_dotenv
from app.core.config import settings

print(f"Current Directory: {os.getcwd()}")
print(f"SECRET_KEY in settings: {settings.SECRET_KEY}")
print(f"SECRET_KEY in os.environ: {os.environ.get('SECRET_KEY')}")

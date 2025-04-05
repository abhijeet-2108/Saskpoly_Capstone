import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Use a better key in prod
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql://username:password@localhost/pentest_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
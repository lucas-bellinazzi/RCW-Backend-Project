import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI_POSTGRES")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

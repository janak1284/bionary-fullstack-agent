import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "DEV_SECRET_SHOULD_BE_LONG")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

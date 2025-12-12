# backend/database.py
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Use Neon if available, otherwise fall back to local sqlite (for dev)
DATABASE_URL = os.getenv("NEON_DB_URL") or "sqlite:///./database.db"

# Extra connect_args only for sqlite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔴 THIS is what was missing / broken
Base = declarative_base()


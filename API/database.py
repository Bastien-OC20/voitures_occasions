import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Assurez-vous que le répertoire de la base de données existe
os.makedirs(os.path.dirname("./data/db/voitures_aramisauto_final.db"), exist_ok=True)

DATABASE_URL = "sqlite:///./data/db/voitures_aramisauto_final.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
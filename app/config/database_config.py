import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
local_session = sessionmaker(autoflush=False, bind=engine)

try:
    db = local_session()
    print("Base de datos conectada")
except SQLAlchemyError as e:
    print("Error al conectar a la base de datos:", e)
    db = None
finally:
    if db:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

from dotenv import load_dotenv
load_dotenv()


class BaseDeDatos():
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.passwd = os.getenv("DB_PASS")
        self.port = os.getenv("DB_PORT")
        self.name = os.getenv("DB_NAME")

    def iniciar_conexion(self):
        SQLALCHEMY_DATABASE_URL = f'mariadb+mariadbconnector://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.name}'
        print(SQLALCHEMY_DATABASE_URL)
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_recycle=3600,
                echo_pool=True,
                echo=True,
                pool_timeout=30,
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base = declarative_base()
            return Base, SessionLocal, engine
        except Exception as err:
            print(str(err))
        

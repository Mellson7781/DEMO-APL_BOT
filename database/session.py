from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


#Загрузка из .env
load_dotenv()


#Получение url бд из .env 
DB_URL = os.getenv("DB_URL")


#Создание двигателя
engine = create_engine(url=DB_URL, echo=True)


#Создание сессии в бд
Session = sessionmaker(bind=engine)
session = Session()
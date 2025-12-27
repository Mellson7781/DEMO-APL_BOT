from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (BigInteger, String, 
                        DateTime, Text, func)
from database.session import engine, session
from datetime import datetime


class Base(DeclarativeBase):
    pass


#Таблица applications
class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String(40))
    service: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(40))
    contact: Mapped[str] = mapped_column(String())
    comment: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(10), default='new')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

#Создаем все таблицы
Base.metadata.create_all(engine)
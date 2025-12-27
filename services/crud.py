from sqlalchemy import func
from database.session import session
from database.models import Applications


#Добавление данных в бд
def new_applications(
        tg_id: int, tg_username:str,
        service: str, name: str,
        contact: str, comment: str):
    try: 
        session.add(Applications(
            user_id = tg_id, tg_username=tg_username,
            service = service, name = name,
            contact = contact, comment = comment))
        session.commit()
    except:
        session.rollback()


#Получение всех заявок по статусу
def all_applications_in_status(status: str):
    all_apl = session.query(Applications).filter(Applications.status == status).all()
    return all_apl


#Получение конкретной application
def application_id(id: int):
    return session.query(Applications).filter(Applications.id == id).first()


#Изменение статуса заявки
def edit_status(status: str, id: int):
    try:
        apl = application_id(id=id)
        apl.status = status
        session.commit()
    except:
        session.rollback()


#Получение списка для статистики
def list_static() -> list:
    count_all = session.query(func.count(Applications.id)).scalar()
    count_new = session.query(func.count(Applications.id)).filter(Applications.status=='new').scalar()
    count_work = session.query(func.count(Applications.id)).filter(Applications.status=='in_work').scalar()
    count_done = session.query(func.count(Applications.id)).filter(Applications.status=='done').scalar()
    return [count_all, count_new, count_work, count_done]
from aiogram.fsm.state import StatesGroup, State


class Services(StatesGroup):
    name = State()
    contact = State()
    description = State()


class Applic(StatesGroup):
    apl_id = State()
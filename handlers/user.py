from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from keyboards.inline import menu_services, menu_in_serv
from states.form import Services
from services.crud import new_applications

#создание роутера
user_rt = Router()


#Обработка команды старт
@user_rt.message(CommandStart())
async def start(message: Message):
    await message.answer("Здравствуйте! 👋\nВыберите услугу:",
                        reply_markup=menu_services)


#Обработка web
@user_rt.callback_query(F.data == 'web')
async def services_web(query: CallbackQuery, state:FSMContext):
    await state.update_data(services='Разработка сайта')
    await query.answer('')
    await query.message.answer('Отлично!')
    await query.message.answer('Как вас зовут?')
    await state.set_state(Services.name)


#Обработка bot
@user_rt.callback_query(F.data == 'bot')
async def services_bot(query: CallbackQuery, state:FSMContext):
    await state.update_data(services='Telegram-бот')
    await query.answer('')
    await query.message.answer('Отлично!')
    await query.message.answer('Как вас зовут?')
    await state.set_state(Services.name)


#Обработка info
@user_rt.callback_query(F.data == 'info')
async def services_info(query: CallbackQuery, state:FSMContext):
    await state.update_data(services='Консультация')
    await query.answer('')
    await query.message.answer('Отлично!')
    await query.message.answer('Как вас зовут?')
    await state.set_state(Services.name)


#Обработка State.name
@user_rt.message(Services.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите контакт для связи (телефон или @username):')
    await state.set_state(Services.contact)


#Обработка State.contact
@user_rt.message(Services.contact)
async def contacts(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer('Опишите задачу или оставьте комментарий:')
    await state.set_state(Services.description)


#Обработка State.description
@user_rt.message(Services.description)
async def descript(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(
        'Проверьте данные:\n\n'
        f'Услуга: {data.get("services")}\n'
        f"Имя: {data.get("name")}\n"
        f"Контакт: {data.get("contact")}\n"
        f"Комментарий: {data.get("description")}\n\n"
        "Отправить заявку?",
        reply_markup=menu_in_serv)


#Обработка message
@user_rt.callback_query(F.data == 'message')
async def mes(query: CallbackQuery, state:FSMContext):
    await query.message.delete()
    data = await state.get_data()
    await query.answer("")
    new_applications(
        tg_id=query.message.from_user.id,
        tg_username=query.message.from_user.username,
        service=data.get('services'), name=data.get('name'),
        contact=data.get('contact'), comment=data.get('description'))
    await query.message.answer(
        "Спасибо! 🙌\n"
        "Ваша заявка принята.\n"
        "Мы свяжемся с вами в ближайшее время.")
    await state.clear()


#Обработка no_message
@user_rt.callback_query(F.data == 'no_message')
async def no_mes(query: CallbackQuery, state:FSMContext):
    await query.message.delete()
    await state.clear()
    await query.answer("")
    await query.message.answer("Начнем сначала!:",
                        reply_markup=menu_services)
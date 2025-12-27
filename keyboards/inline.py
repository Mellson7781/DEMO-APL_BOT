from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from services.crud import all_applications_in_status

#Кнопки клиент панели:
#Доступные услуги
menu_services = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📦 Разработка сайта", callback_data='web')],
    [InlineKeyboardButton(text="🤖 Telegram-бот", callback_data='bot')],
    [InlineKeyboardButton(text="📞 Консультация", callback_data='info')]
])


#Выбор действий 
menu_in_serv = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Отправить', callback_data="message"),
     InlineKeyboardButton(text='❌ Отменить', callback_data="no_message")]
])


#Кнопки админ панели:
#Админ меню
menu_admin =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📥 Новые заявки', callback_data='new')],
    [InlineKeyboardButton(text='🛠 В работе', callback_data='work')],
    [InlineKeyboardButton(text='✅ Завершённые', callback_data='done')],
    [InlineKeyboardButton(text='🔍 Найти заявку', callback_data='src')],
    [InlineKeyboardButton(text='📊 Статистика', callback_data='static')]
])


#Создание кнопок для списков заявок new
def kb_status_new():
    builder = InlineKeyboardBuilder()
    applications = all_applications_in_status('new')
    for apl in applications:
        builder.button(text=f'#{apl.id} - {apl.service}',
                       callback_data=f'new_{apl.id}')
    builder.button(text='🔙 Назад', callback_data='back')
    builder.adjust(1)
    return builder.as_markup()


#Создание кнопок для списков заявок in_work
def kb_status_in_work():
    builder = InlineKeyboardBuilder()
    applications = all_applications_in_status('in_work')
    for apl in applications:
        builder.button(text=f'#{apl.id} - {apl.service}',
                       callback_data=f'work_{apl.id}')
    builder.button(text='🔙 Назад', callback_data='back')
    builder.adjust(1)
    return builder.as_markup()


#Создание кнопок для списков заявок done
def kb_status_done():
    builder = InlineKeyboardBuilder()
    applications = all_applications_in_status('done')
    for apl in applications:
        builder.button(text=f'#{apl.id} - {apl.service}',
                       callback_data=f'done_{apl.id}')
    builder.button(text='🔙 Назад', callback_data='back')
    builder.adjust(1)
    return builder.as_markup()


#Меню статусов new
menu_status_new = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛠 В работу', callback_data='in_work')],
    [InlineKeyboardButton(text='✅ Завершить', callback_data='is_done')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])


#Меню статусов in_work
menu_status_work = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Завершить', callback_data='is_done')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])


#Меню назад
menu_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])
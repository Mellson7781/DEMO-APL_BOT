from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards.inline import (menu_admin, kb_status_new,
                              kb_status_done, kb_status_in_work,
                              menu_status_new, menu_status_work, menu_back)
from services.crud import application_id, edit_status, list_static
from states.form import Applic


#Админ роутер
admin_rt = Router()


#Права админа, нужно указать tg id
admin = 5106745657


#Вхождение в меню админа
@admin_rt.message(Command('admins'))
async def in_admins(message: Message):
    user_id = message.from_user.id
    if user_id == admin:
        await message.answer(
            'Админ-панель 🛠\n'
            'Выберите действие:',
            reply_markup=menu_admin)
    else:
        await message.answer("Отказано в доступе!")


#Кнопка назад
@admin_rt.callback_query(F.data == 'back')
async def is_back(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(
            'Админ-панель 🛠\n'
            'Выберите действие:',
            reply_markup=menu_admin)


#Обработка new
@admin_rt.callback_query(F.data == 'new')
async def button_new(query: CallbackQuery):
    await query.message.delete()
    await query.answer('')
    await query.message.answer('Заявки со статусом: NEW',
                               reply_markup=kb_status_new())


@admin_rt.callback_query(F.data.startswith("new_"))
async def new_call(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.answer('')
    id = int(query.data.split('_')[1])
    app = application_id(id=id)
    await query.message.answer(
        f'Заявка #{app.id}\n\n'
        f'Услуга: {app.service}\n'
        f'Имя: {app.name}\n'
        f'Контакт: {app.contact}\n'
        f'Комментарий:\n{app.comment}\n\n'
        f'Статус: {app.status}\n'
        f'Создана: {app.created_at}',
        reply_markup=menu_status_new)
    await state.update_data(id=id)
    

#Обработка work
@admin_rt.callback_query(F.data == 'work')
async def button_new(query: CallbackQuery):
    await query.message.delete()
    await query.answer('')
    await query.message.answer('Заявки со статусом: IN_WORK',
                               reply_markup=kb_status_in_work())


@admin_rt.callback_query(F.data.startswith("work_"))
async def work_call(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.answer('')
    id = int(query.data.split('_')[1])
    app = application_id(id=id)
    await query.message.answer(
        f'Заявка #{app.id}\n\n'
        f'Услуга: {app.service}\n'
        f'Имя: {app.name}\n'
        f'Контакт: {app.contact}\n'
        f'Комментарий:\n{app.comment}\n\n'
        f'Статус: {app.status}\n'
        f'Создана: {app.created_at}',
        reply_markup=menu_status_work)
    await state.update_data(id=id)


#Обработка work
@admin_rt.callback_query(F.data == 'done')
async def button_new(query: CallbackQuery):
    await query.message.delete()
    await query.answer('')
    await query.message.answer('Заявки со статусом: DONE',
                               reply_markup=kb_status_done())


@admin_rt.callback_query(F.data.startswith("done_"))
async def work_call(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.answer('')
    id = int(query.data.split('_')[1])
    app = application_id(id=id)
    await query.message.answer(
        f'Заявка #{app.id}\n\n'
        f'Услуга: {app.service}\n'
        f'Имя: {app.name}\n'
        f'Контакт: {app.contact}\n'
        f'Комментарий:\n{app.comment}\n\n'
        f'Статус: {app.status}\n'
        f'Создана: {app.created_at}',
        reply_markup=menu_back)
    await state.update_data(id=id)


#Обработка in_work
@admin_rt.callback_query(F.data == 'in_work')
async def in_work(query: CallbackQuery, state: FSMContext):
    await query.answer('')
    data = await state.get_data()
    id = data.get('id')
    await query.message.delete()

    edit_status(status='in_work', id=id)
    await query.message.answer(f"Статус заявки #{id} изменён на IN_WORK")
    await state.clear()


#Обработка is_done
@admin_rt.callback_query(F.data == 'is_done')
async def is_done(query: CallbackQuery, state: FSMContext):
    await query.answer('')
    data = await state.get_data()
    id = data.get('id')
    await query.message.delete()

    edit_status(status='done', id=id)
    await query.message.answer(f"Статус заявки #{id} изменён на DONE")
    await state.clear()


#Обработка src
@admin_rt.callback_query(F.data == 'src')
async def is_src(query: CallbackQuery, state: FSMContext):
    await query.answer('')
    await query.message.delete()
    await query.message.answer("Введите ID заявки:")
    await state.set_state(Applic.apl_id)


@admin_rt.message(Applic.apl_id)
async def src_answer(message: Message):
    try:
        src_id = int(message.text)
        app = application_id(src_id)
        if app != None:
            await message.answer(
            f'Заявка #{app.id}\n\n'
            f'Услуга: {app.service}\n'
            f'Имя: {app.name}\n'
            f'Контакт: {app.contact}\n'
            f'Комментарий:\n{app.comment}\n\n'
            f'Статус: {app.status}\n'
            f'Создана: {app.created_at}', 
            reply_markup=menu_back)
        else:
            await message.answer("Такой заявки нет!",
                             reply_markup=menu_admin)
    except ValueError:
        await message.answer("Вы написали не число!",
                             reply_markup=menu_admin)


#Обработка static
@admin_rt.callback_query(F.data == 'static')
async def static(query: CallbackQuery):
    st = list_static()
    await query.answer("") 
    await query.message.delete()
    await query.message.answer(
        f"📊 Статистика заявок\n\n"
        f"Всего: {st[0]}\n"
        f"Новые: {st[1]}\n"
        f"В работе: {st[2]}\n"
        f"Завершённые: {st[3]}")
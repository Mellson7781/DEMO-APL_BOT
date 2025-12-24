from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os, asyncio


#Загрузка из .env
load_dotenv()


#Получение токина бота из .env
BOT_TOKEN = os.getenv("BOT_TOKEN") 


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


#Функция для запуска бота
async def main():
    #Удаляем все накполеные обращения при запуске
    await bot.delete_webhook(drop_pending_updates=True)
    #Подключение роутеров
    #dp.include_routers()
    #Запуск polling (Проще говоря запуск бота)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
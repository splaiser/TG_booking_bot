import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'начнём', 'начнем'])
async def send_welcome(message: types.Message):
    await message.answer("Привет новый пользователь!\nДавай забронируем номер вместе!")


@dp.message_handler(commands=["booking", "бронь", "забронировать", "б"])
async def booking():
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

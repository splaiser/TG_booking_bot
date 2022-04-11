from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import DB


async def send_welcome(message: types.Message):
    await message.answer("Привет новый пользователь!\nДавай забронируем номер вместе!")


async def rooms_list(message: types.Message):
    await message.answer("Вот список номеров нашего отеля")
    await DB.get_rooms_list(message)

async def booking(user_id: types.User):
    print(user_id)
    await bot.send_message(user_id['from']['id'], text=f"Ваше имя: {user_id['from']['first_name']}")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'начнём', 'начнем'])
    dp.register_message_handler(rooms_list, commands=['номера', 'rooms'])
    # dp.register_message_handler()
    dp.register_message_handler(booking, commands=["инфо"])






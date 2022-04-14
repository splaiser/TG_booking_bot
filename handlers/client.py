from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base.DB import get_rooms_list
from aiogram.types import InputMediaPhoto, InputMedia, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton

async def send_welcome(message: types.Message):
    await message.answer("Привет новый пользователь!\nДавай забронируем номер вместе!",
                         reply_markup=kb_client)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('booking '))
async def del_callback(callback_query: types.CallbackQuery):
    await delete_apart(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


async def rooms_list(message: types.Message):
    await message.answer("Вот список номеров нашего отеля")
    Apart = await get_rooms_list()
    for _apart in Apart:
        media = []
        for photo in _apart.aparts_photo:
            media.append(InputMediaPhoto(photo.photo_url))
        try:
            await bot.send_media_group(message.from_user.id, media)
            await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                         f"Тип номера: {_apart.apart_type}\n"
                                                         f"Описание: {_apart.apart_description}\n"
                                                         f"Цена: {_apart.apart_price}")
            await bot.send_message(message.from_user.id, text='^^^^^^^^^^^^^^^^^^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(text=f'Забронировать номер : {_apart.apart_name}'
                                                            , callback_data=f'booking {_apart.apart_name}')))
        except:
            await bot.send_photo(message.from_user.id, media)
            await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                         f"Тип номера: {_apart.apart_type}\n"
                                                         f"Описание: {_apart.apart_description}\n"
                                                         f"Цена: {_apart.apart_price}")
            await bot.send_message(message.from_user.id, text='^^^^^^^^^^^^^^^^^^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Удалить Номер : {_apart.apart_name}',
                                                            callback_data=f'booking {_apart.apart_name}')))


async def booking(user_id: types.User):
    await bot.send_message(user_id['from']['id'], text=f"Ваше имя: {user_id['from']['first_name']}")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'начнём', 'начнем'])
    dp.register_message_handler(rooms_list, commands=['номера', 'rooms'])
    dp.register_message_handler(booking, commands=["инфо"])
    # dp.register_message_handler()






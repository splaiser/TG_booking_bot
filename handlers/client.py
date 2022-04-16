from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards.client_kb import button_case_client
from aiogram.types import ReplyKeyboardRemove
from data_base.DB import get_rooms_list, get_room
from aiogram.types import InputMediaPhoto, InputMedia, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base.DB import book_room


class FSMCreateBook(StatesGroup):

    name = State()
    month = State()
    time = State()


async def send_welcome(message: types.Message):
    await message.answer("Привет новый пользователь!\nДавай забронируем номер вместе!",
                         reply_markup=button_case_client)


async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Можете начать заного!")


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('time '), state=FSMCreateBook.time)
async def get_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = callback_query.data.replace("time ", "")
        await bot.send_message(callback_query.from_user.id, text=f"Поздравляю!\n"
                                                                 f"Вы забронировали номер: {data['name']}\n"                    
                                                                 f"Месяц: {data['month']}\n"
                                                                 f"Время: {data['time']}")
        await book_room(data['name'], data['month'], data['time'])

        await state.finish()
        await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('month '), state=FSMCreateBook.month)
async def get_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = callback_query.data.replace("month ", "")
        await bot.send_message(callback_query.from_user.id, text="На какой месяц вы бы хотели забронировать номер?",
                               reply_markup=InlineKeyboardMarkup(row_width=3)
                               .add(InlineKeyboardButton(text='12.00', callback_data=f'time 12.00'))
                               .add(InlineKeyboardButton(text='12.30', callback_data=f'time 12.30'))
                               .add(InlineKeyboardButton(text='13.00', callback_data=f'time 13.00'))
                               .add(InlineKeyboardButton(text='13.30', callback_data=f'time 13.30'))
                               .add(InlineKeyboardButton(text='14.00', callback_data=f'time 14.00'))
                               .add(InlineKeyboardButton(text='14.30', callback_data=f'time 14.30'))
                               .add(InlineKeyboardButton(text='15.30', callback_data=f'time 15.30'))
                               .add(InlineKeyboardButton(text='16.00', callback_data=f'time 16.00'))
                               .add(InlineKeyboardButton(text='16.30', callback_data=f'time 16.30'))
                               .add(InlineKeyboardButton(text='17.00', callback_data=f'time 17.00'))
                               .add(InlineKeyboardButton(text='17.30', callback_data=f'time 17.30'))
                               .add(InlineKeyboardButton(text='18.00', callback_data=f'time 18.00'))
                               )
        await FSMCreateBook.next()
        await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('booking '), state=FSMCreateBook.name)
async def get_booking(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = callback_query.data.replace("booking ", "")
        await bot.send_message(callback_query.from_user.id, text="На какой месяц вы бы хотели забронировать номер?",
                               reply_markup=InlineKeyboardMarkup(row_width=3)
                               .add(InlineKeyboardButton(text='Январь', callback_data=f'month Январь'))
                               .add(InlineKeyboardButton(text='Февраль', callback_data=f'month Февраль'))
                               .add(InlineKeyboardButton(text='Март', callback_data=f'month Март'))
                               .add(InlineKeyboardButton(text='Апрель', callback_data=f'month Апрель'))
                               .add(InlineKeyboardButton(text='Май', callback_data=f'month Май'))
                               .add(InlineKeyboardButton(text='Июнь', callback_data=f'month Июнь'))
                               .add(InlineKeyboardButton(text='Июль', callback_data=f'month Июль'))
                               .add(InlineKeyboardButton(text='Август', callback_data=f'month Август'))
                               .add(InlineKeyboardButton(text='Сентябрь', callback_data=f'month Сентябрь'))
                               .add(InlineKeyboardButton(text='Октрябрь', callback_data=f'month Октрябрь'))
                               .add(InlineKeyboardButton(text='Ноябрь', callback_data=f'month Ноябрь'))
                               .add(InlineKeyboardButton(text='Декабрь', callback_data=f'month Декабрь'))
                               )
        await FSMCreateBook.next()
        await callback_query.answer()


async def rooms_list(message: types.Message, state: FSMContext):
    await FSMCreateBook.name.set()
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
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(rooms_list, commands=['номера', 'rooms'], state=None)
    dp.register_message_handler(booking, commands=["инфо"])
    # dp.register_message_handler()

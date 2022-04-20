from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards.client_kb import button_case_client, button_case_get_contact
from aiogram.types import ReplyKeyboardRemove
from data_base.DB import get_rooms_list, get_room
from aiogram.types import InputMediaPhoto, InputMedia, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base.DB import book_room, get_bookig_list, get_free_time_of_room


class FSMCreateBook(StatesGroup):
    name = State()
    month = State()
    day = State()
    time = State()
    phone = State()


async def send_welcome(message: types.Message):
    await message.answer(f"👋 Привет {message.from_user.full_name}!\n"
                         f"Давай забронируем номер вместе!\n\n"
                         f"🏙 /rooms - Команда с помощью которой ты сможешь посмотреть все номера.\n"
                         f"ℹ /info - Команда с помощью которой ты сможешь узнать все контактные данные,"
                         f" адрес и прочую информацию о нас.\n"
                         f"🚫 /cancel - Если что-то пошло не так всегда"
                         f" можешь отменить твоё действие и начать с начала!",
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
        await bot.send_message(callback_query.from_user.id,
                               text='Нам понадобятся ваши контактные данные',
                               reply_markup=button_case_get_contact)
        await FSMCreateBook.next()
        await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('day '), state=FSMCreateBook.day)
async def get_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = callback_query.data.replace("day ", "")
        free_time = await get_free_time_of_room(data['month'], data['day'])
        button_case = InlineKeyboardMarkup(row_width=5)
        if free_time is None:
            await bot.send_message(callback_query.from_user.id, text='На данное число нету свободного времени,'
                                                                     ' попробуйте выбрать другой день')
            await state.finish()
        else:
            for time in free_time:
                button_case.insert(InlineKeyboardButton(text=f'{time}', callback_data=f'time {time}'))
            await bot.send_message(callback_query.from_user.id, text="Выберете время.",
                                   reply_markup=button_case
                                   )
            await FSMCreateBook.next()
            await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('month '), state=FSMCreateBook.month)
async def get_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = callback_query.data.replace("month ", "")
        button_case = InlineKeyboardMarkup(row_width=5)
        month_with_31days = ['Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь']
        month_with_30days = ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']
        if data['month'] == 'Февраль':
            for day in range(1, 29):
                button_case.insert(InlineKeyboardButton(text=f'{day}', callback_data=f'day {day}'))
        elif data['month'] in month_with_31days:
            for day in range(1, 31):
                button_case.insert(InlineKeyboardButton(text=f'{day}', callback_data=f'day {day}'))
        elif data['month'] in month_with_30days:
            for day in range(1, 30):
                button_case.insert(InlineKeyboardButton(text=f'{day}', callback_data=f'day {day}'))

        await bot.send_message(callback_query.from_user.id, text="Теперь нужно выбрать число.",
                               reply_markup=button_case)
        await FSMCreateBook.next()
        await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('booking '), state=FSMCreateBook.name)
async def get_booking(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = callback_query.data.replace("booking ", "")
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                      'Октябрь', 'Ноябрь', 'Декабрь']
        button_case = InlineKeyboardMarkup(row_width=3)
        for month in month_list:
            button_case.insert(InlineKeyboardButton(text=f'{month}', callback_data=f'month {month}'))
        await bot.send_message(callback_query.from_user.id, text="На какой месяц вы бы хотели забронировать номер?",
                               reply_markup=button_case)
        await FSMCreateBook.next()
        await callback_query.answer()


async def rooms_list(message: types.Message):
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
            await bot.send_message(message.from_user.id, text='👆👆👆',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton(text=f'Забронировать номер'
                                                            , callback_data=f'booking {_apart.apart_name}')))

        except:
            await bot.send_photo(message.from_user.id, media)
            await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                         f"Тип номера: {_apart.apart_type}\n"
                                                         f"Описание: {_apart.apart_description}\n"
                                                         f"Цена: {_apart.apart_price}")
            await bot.send_message(message.from_user.id, text='👆👆👆',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton(f'Забронировать номер',
                                                            callback_data=f'booking {_apart.apart_name}')))


@dp.message_handler(content_types=['contact'],
                    state=FSMCreateBook.phone)
async def get_phone(message: types.Contact, state: FSMContext):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    async with state.proxy() as data:
        await book_room(data['name'], data['month'], data['day'], data['time'], message.from_user.full_name,
                        message.from_user.id, message.contact.phone_number)

        await bot.send_message(message.from_user.id, text=f"Поздравляю!\n"
                                                          f"Вы забронировали номер: {data['name']}\n"
                                                          f"Месяц: {data['month']}\n"
                                                          f"Время: {data['time']}\n"
                                                          f"Связаться с вами можно по номеру: "
                                                          f"{message.contact.phone_number}",
                               reply_markup=button_case_client)
        await state.finish()


async def info(user_id: types.User):
    await bot.send_message(user_id['from']['id'], text=f"📓📓📓ИНФОРМАЦИЯ О НАС📓📓📓\n"
                                                       f"Мы находимся - ...........\n\n"
                                                       f"☎☎☎СВЯЗАТЬСЯ С НАМИ МОЖНО☎☎☎\n"
                                                       f"Телеграм - ...............\n"
                                                       f"Номер телефона - .........\n")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(rooms_list, commands=['rooms'], state=None)

    dp.register_message_handler(info, commands=["info"])

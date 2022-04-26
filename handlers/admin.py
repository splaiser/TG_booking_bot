from aiogram import types, Dispatcher

from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base.DB import add_apartment, delete_apart, get_rooms_list, get_all_order, delete_booking
from keyboards import admin_kb
from typing import List
from aiogram.types import InputMediaPhoto, InputMedia, MediaGroup, InlineKeyboardMarkup, InlineKeyboardButton

ID = None


class FSMAdminCreate(StatesGroup):
    photo = State()
    type = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Администратор идентефицирован.",
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminCreate.photo.set()
        await message.reply('Загрузите фото (Больше 1 и не забудь указать "сжать изображение)')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")


async def load_photo(message: types.Message, album: List[types.Message], state: FSMContext):
    downloading_list = []
    media_group = types.MediaGroup()
    if message.from_user.id == ID:
        async with state.proxy() as data:
            for obj in album:
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                    downloading_list.append(file_id)
                else:
                    file_id = obj[obj.content_type].file_id

                try:
                    # We can also add a caption to each file by specifying `"caption": "text"`
                    media_group.attach({"media": file_id, "type": obj.content_type})
                except ValueError:
                    return await message.answer("This type of album is not supported by aiogram.")

            # await message.answer_media_group(media_group)

            data['photo'] = downloading_list
            await FSMAdminCreate.next()
            await message.reply("Теперь тип номера")


async def load_type(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['type'] = message.text
            await FSMAdminCreate.next()
            await message.reply("Теперь укажите название номера")


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
            await FSMAdminCreate.next()
            await message.reply("Введите описание номера")


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
            await FSMAdminCreate.next()
            await message.reply("Введите цену номера")


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
            add_apartment(data['name'], data['price'], data['type'], data['description'], data['photo'])
        await state.finish()
        await message.answer('Данные загруженны.')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback(callback_query: types.CallbackQuery):
    await delete_apart(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


async def del_start(message: types.Message):
    if message.from_user.id == ID:
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
                                           InlineKeyboardButton(text=f'Удалить Номер : {_apart.apart_name}',
                                                                callback_data=f'del {_apart.apart_name}')))
            except:
                await bot.send_photo(message.from_user.id, media)
                await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                             f"Тип номера: {_apart.apart_type}\n"
                                                             f"Описание: {_apart.apart_description}\n"
                                                             f"Цена: {_apart.apart_price}")
                await bot.send_message(message.from_user.id, text='^^^^^^^^^^^^^^^^^^^^',
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton(f'Удалить Номер : {_apart.apart_name}',
                                                                callback_data=f'del {_apart.apart_name}')))


async def get_last_order_info(message: types.Message):
    if message.from_user.id == ID:
        all_order = get_all_order()
        if len(all_order) == 1:
            last_order = all_order[0]
            text = f"Заказ: {last_order.booking_id}\n" \
                   f"Номер: {last_order.apart_name}\n" \
                   f"Заказчик: {last_order.name}. ID {last_order.user_id}\n" \
                   f"Номер телефона: {last_order.phone}\n" \
                   f"Дата брони: {last_order.month} {last_order.day}\n" \
                   f"Время брони: {last_order.time}"
            await bot.send_message(message.from_user.id, text=text, reply_markup=InlineKeyboardMarkup() \
                                   .add(
                InlineKeyboardButton(text="Удалить бронь", callback_data=f"delbooking {last_order.booking_id}")))
        elif len(all_order) > 1:
            last_order = all_order[-1]
            text = f"Заказ: {last_order.booking_id}\n" \
                   f"Номер: {last_order.apart_name}\n" \
                   f"Заказчик: {last_order.name}. ID {last_order.user_id}\n" \
                   f"Номер телефона: {last_order.phone}\n" \
                   f"Дата брони: {last_order.month} {last_order.day}\n" \
                   f"Время брони: {last_order.time}"

            await bot.send_message(message.from_user.id, text=text, reply_markup=InlineKeyboardMarkup() \
                                   .add(
                InlineKeyboardButton(text="Удалить бронь", callback_data=f"delbooking {last_order.booking_id}")))
        else:
            await bot.send_message(message.from_user.id, text="На данный момент бронированний нет.")


async def get_all_booking(message: types.Message):
    if message.from_user.id == ID:
        if get_all_order():
            for _booking in get_all_order():
                text = f"Заказ: {_booking.booking_id}\n" \
                       f"Номер: {_booking.apart_name}\n" \
                       f"Заказчик: {_booking.name}. ID {_booking.user_id}\n" \
                       f"Номер телефона: {_booking.phone}\n" \
                       f"Дата брони: {_booking.month} {_booking.day}\n" \
                       f"Время брони: {_booking.time}"
                await bot.send_message(message.from_user.id, text=text, reply_markup=InlineKeyboardMarkup() \
                                       .add(
                    InlineKeyboardButton(text="Удалить бронь", callback_data=f"delbooking {_booking.booking_id}")))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delbooking '))
async def del_booking(callback_query: types.CallbackQuery):
    await delete_booking(callback_query.data.replace("delbooking ", ""))
    await callback_query.answer(text=f'Бронь: {callback_query.data.replace("delbooking ", "")} удалена.',
                                show_alert=True)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], user_id=455608043)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['any'], is_media_group=True, state=FSMAdminCreate.photo)
    dp.register_message_handler(load_type, state=FSMAdminCreate.type)
    dp.register_message_handler(load_name, state=FSMAdminCreate.name)
    dp.register_message_handler(load_description, state=FSMAdminCreate.description)
    dp.register_message_handler(load_price, state=FSMAdminCreate.price)
    dp.register_message_handler(del_start, commands=['удалить'])
    dp.register_message_handler(get_last_order_info, commands=['последняя_бронь'])
    dp.register_message_handler(get_last_order_info, commands=['вся_бронь'])

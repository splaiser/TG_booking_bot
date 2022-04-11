from aiogram import types, Dispatcher
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base.DB import add_apartment
from keyboards import admin_kb

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
    await bot.send_message(message.from_user.id, "Администратор идентефицирован.", reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminCreate.photo.set()
        await message.reply('Загрузи фото ПО ОДНОМУ ФОТО (Не забудь указать "сжать изображение"')


async def load_photo(message: types.Message, state: FSMContext):
    downloading_list = []
    if message.from_user.id == ID:
        async with state.proxy() as data:
            for photo in message:
                downloading_list..photo_id)
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

        async with state.proxy() as data:
            add_apartment(data['name'], data['price'], data['type'], data['description'], data['photo'])
        await state.finish()
        await message.answer('Данные загруженны.')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], user_id=455608043)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdminCreate.photo)
    dp.register_message_handler(load_type, state=FSMAdminCreate.type)
    dp.register_message_handler(load_name, state=FSMAdminCreate.name)
    dp.register_message_handler(load_description, state=FSMAdminCreate.description)
    dp.register_message_handler(load_price, state=FSMAdminCreate.price)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_start = KeyboardButton('/start')
button_info = KeyboardButton('/info')
button_cancel = KeyboardButton('/cancel')
button_get_room_list = KeyboardButton('/rooms')
button_booking = KeyboardButton('/booking')
button_get_contact = KeyboardButton('Отправить контакт', request_contact=True)

button_case_client = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_client.insert(button_start).insert(button_info)\
    .insert(button_get_room_list).insert(button_booking).insert(button_cancel)

button_case_get_contact = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_get_contact.add(button_get_contact)


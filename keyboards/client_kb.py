from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_info = KeyboardButton('/info')
button_cancel = KeyboardButton('/cancel')
button_get_room_list = KeyboardButton('/rooms')
button_get_contact = KeyboardButton('Отправить контакт', request_contact=True)

button_case_client = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_client.add(button_info).add(button_get_room_list).add(button_cancel)

button_case_get_contact = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_get_contact.add(button_get_contact)


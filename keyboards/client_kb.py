from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


button_info = KeyboardButton('/инфо')
button_cancel = KeyboardButton('/отмена')
button_get_room_list = KeyboardButton('/номера')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button_info).add(button_get_room_list).add(button_cancel)
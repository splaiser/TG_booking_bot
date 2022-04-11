from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/start')
b2 = KeyboardButton('/инфо')
b3 = KeyboardButton('/отмена')
button_get_room_list = KeyboardButton('/номера')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(button_get_room_list).add(b3)
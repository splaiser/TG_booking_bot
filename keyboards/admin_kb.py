from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_last_order = KeyboardButton("/последняя_бронь")
button_all_order = KeyboardButton('/вся_бронь')
button_load = KeyboardButton('/загрузить')
button_delete = KeyboardButton('/удалить')
button_cancel = KeyboardButton("/отмена")


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_last_order)\
    .add(button_all_order)\
    .add(button_load)\
    .add(button_delete)\
    .add(button_cancel)



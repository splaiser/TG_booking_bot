from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_load = KeyboardButton('/загрузить')
button_moderator = KeyboardButton('/moderator')
button_cancel = KeyboardButton("/отмена")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_cancel)


inl_button = InlineKeyboardMarkup(row_width=1)
button_delete = InlineKeyboardButton(text='удалить', callback_data='delete_apartment')
inl_button.add(button_delete)

# button_load = InlineKeyboardButton(text="Загрузить", callback_data='/загрузить')
# button_delete = InlineKeyboardButton(text="Удалить", callback_data='/удалить')
# button_cancel = InlineKeyboardButton(text="Отмена", callback_data='/отмена')

inl_button.add(button_load, button_delete, button_cancel)
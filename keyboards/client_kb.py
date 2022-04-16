from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_info = KeyboardButton('/инфо')
button_cancel = KeyboardButton('/отмена')
button_get_room_list = KeyboardButton('/номера')

button_case_client = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_client.add(button_info).add(button_get_room_list).add(button_cancel)

# bn_mth_January = InlineKeyboardButton(text='Январь', callback_data=f'{booking_data}')
#
#
# button_month_February = InlineKeyboardButton(text='Февраль', callbakc_data=f'{booking_data}')


# button_month_March = InlineKeyboardButton(text='Март',
#                                           callback_data='month Март , apart {callback_query.data.replace("booking '
#                                                         '", "")}')
# button_month_April = InlineKeyboardButton(text='Апрель',
#                                           callback_data='month Апрель , apart {callback_query.data.replace("booking '
#                                                         '", "")}')
# button_month_May = InlineKeyboardButton(text='Май',
#                                         callback_data='month Май , apart {callback_query.data.replace("booking ", "")}')
# button_month_June = InlineKeyboardButton(text='Июнь',
#                                          callback_data='month Июнь , apart {callback_query.data.replace("booking ", '
#                                                        '"")}')
# button_month_July = InlineKeyboardButton(text='Июль',
#                                          callback_data='month Июль , apart {callback_query.data.replace("booking ", '
#                                                        '"")}')
# button_month_August = InlineKeyboardButton(text='Август',
#                                            callback_data='month Август , apart {callback_query.data.replace("booking '
#                                                          '", "")}')
# button_month_September = InlineKeyboardButton(text='Сентябрь',
#                                               callback_data='month Сентябрь , apart {callback_query.data.replace('
#                                                             '"booking ", "")}')
# button_month_October = InlineKeyboardButton(text='Октябрь',
#                                             callback_data='month Октябрь , apart {callback_query.data.replace('
#                                                           '"booking ", "")}')
# button_month_November = InlineKeyboardButton(text='Ноябрь',
#                                              callback_data='month Ноябрь , apart {callback_query.data.replace('
#                                                            '"booking ", "")}')
# button_month_December = InlineKeyboardButton(text='Декабрь',
#                                              callback_data='month Декабрь , apart {callback_query.data.replace('
#                                                            '"booking ", "")}')

# inline_kb = InlineKeyboardMarkup(row_width=3)
#
#
# inline_kb.add(button_month_January, button_month_February)
# inline_kb.add(button_month_January, button_month_February, button_month_March, button_month_April, button_month_May,
#               button_month_June, button_month_July, button_month_August, button_month_September, button_month_November,
#               button_month_December)

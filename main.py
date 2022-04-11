from aiogram import executor

import data_base.DB
from create_bot import dp
from handlers import client, admin, other
from data_base import DB
from handlers.other import AlbumMiddleware
async def on_startup(_):
    print("Бот Включен")

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)


if __name__ == '__main__':
    data_base.DB.sql_start()
    data_base.DB.create_tables()
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
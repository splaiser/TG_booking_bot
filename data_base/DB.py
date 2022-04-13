from sqlalchemy import Column, Date, Time, String, Integer, ForeignKey, Table, create_engine, select, join, func
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from config import DATABASE
from sqlalchemy.ext.declarative import declarative_base
import sqlite3 as sq
from create_bot import bot
from sqlalchemy.orm import query
from aiogram.types import InputMediaPhoto, InputMedia, MediaGroup

Base = declarative_base()


class User(Base):
    # Таблица с клиентами где хранятся Ники, телефоны, Телеграмм идентефикаторы
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(30))
    phone = Column(String)
    tg_ident = Column(String)


class Apart(Base):
    # Таблица где хранятся Название номера, цена
    __tablename__ = "Apart"

    apart_id = Column(Integer, primary_key=True)
    apart_name = Column(String)
    apart_price = Column(Integer)
    apart_type = Column(String)
    apart_description = Column(String)
    aparts_photo = relationship("Apart_photo", backref="apart", cascade="all, delete, delete-orphan")
    booking = relationship("Booking", secondary="apart_boking")


class Apart_photo(Base):
    # Таблица где хранятся ссылки на фотографии номеров отеля
    __tablename__ = "Apart_photo"

    photo_id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    apart_id = Column(Integer, ForeignKey(Apart.apart_id))


class Booking(Base):
    # Таблица где сохраняются время и дата брони
    __tablename__ = "Booking"

    booking_id = Column(Integer, primary_key=True)
    time = Column(Time)
    date = Column(Date)
    aparts = relationship("Apart", secondary="apart_boking", overlaps="booking")


apart_boking = Table(
    "apart_boking", Base.metadata,
    Column('apart_id', Integer, ForeignKey(Apart.apart_id)),
    Column('booking_id', Integer, ForeignKey(Booking.booking_id)),
)


def create_tables():
    # Создаёт таблицы в БД
    engine = create_engine(URL.create(**DATABASE))
    Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()


def add_apartment(apart_name, apart_price, apart_type, apart_description, apart_photo):
    # Загрузка в БД данных о новом номере.
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    result = []
    new_apart = Apart(apart_name=apart_name, apart_price=apart_price,
                      apart_type=apart_type, apart_description=apart_description)
    for photo in apart_photo:
        result.append(Apart_photo(photo_url=photo))
    new_apart.aparts_photo = result
    # new_apart.aparts_photo = apart_photo
    # new_photo = Apart_photo(photo_url=apart_photo, apart=new_apart)
    session.add(new_apart)
    session.commit()


async def get_rooms_list(message):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    Aparts = session.query(Apart).all()
    for _apart in Aparts:
        media = []
        for photo in _apart.aparts_photo:
            media.append(InputMediaPhoto(photo.photo_url))

        try:
            await bot.send_media_group(message.from_user.id, media)
            await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                         f"Тип номера: {_apart.apart_type}\n"
                                                         f"Описание: {_apart.apart_description}\n"
                                                         f"Цена: {_apart.apart_price}")
        except:
            await bot.send_photo(message.from_user.id, media)
            await bot.send_message(message.from_user.id, f"Номер :{_apart.apart_name}\n"
                                                         f"Тип номера: {_apart.apart_type}\n"
                                                         f"Описание: {_apart.apart_description}\n"
                                                         f"Цена: {_apart.apart_price}")


def delete_apart(name):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    apart_to_delete = session.query(Apart).where(Apart.apart_name == name).one()
    session.delete(apart_to_delete)
    session.commit()



def change_apart_name():
    pass


def change_apart_price():
    pass


def change_apart_type():
    pass


def change_apart_description():
    pass


def change_apart_photo():
    pass


def order_list():
    pass


def get_last_order():
    pass


def sql_start():
    global base
    base = sq.connect('data_base/rooms_booking.db')
    if base:
        print("Data base OK!")


if __name__ == "__main__":
    sql_start()
    create_tables()

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
from sqlalchemy.orm import joinedload

Base = declarative_base()


class User(Base):
    # Таблица с клиентами где хранятся Ники, телефоны, Телеграмм идентефикаторы
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(30))
    phone = Column(String)
    tg_id = Column(String)
    users_booking = relationship("Booking", backref="users_booking", cascade="all, delete, delete-orphan")


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
    time = Column(String)
    day = Column(String)
    month = Column(String)
    aparts = relationship("Apart", secondary="apart_boking", overlaps="booking")
    user_id = Column(Integer, ForeignKey(User.user_id))


apart_boking = Table(
    "apart_boking", Base.metadata,
    Column('apart_id', Integer, ForeignKey(Apart.apart_id)),
    Column('booking_id', Integer, ForeignKey(Booking.booking_id))
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

    session.add(new_apart)
    session.commit()


async def get_rooms_list():
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    Aparts = session.query(Apart).join(Apart_photo).options(joinedload('*')).all()

    return Aparts


async def delete_apart(name):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    on_delete = session.query(Apart).filter(Apart.apart_name == name).first()
    session.delete(on_delete)
    session.commit()


async def get_room(name):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    on_select = session.query(Apart).filter(Apart.apart_name == name).first()
    return on_select


async def book_room(name, month, day, time, user_name, id, phone):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    select_all_user = session.query(User.tg_id).all()
    select_apart = session.query(Apart).filter(Apart.apart_name == name).first()
    new_booking = Booking(month=month, time=time, day=day)

    for user_id in select_all_user:
        if id == int(user_id[0]):
            select_user = session.query(User).filter(User.tg_id == id).first()
            new_booking.aparts.append(select_apart)
            select_user.users_booking.append(new_booking)
            session.add(new_booking, select_user)
            session.commit()
        else:
            new_user = User(name=user_name, phone=phone, tg_id=id)
            new_booking.aparts.append(select_apart)
            new_user.users_booking.append(new_booking)
            session.add(new_booking, new_user)
            session.commit()

    if len(select_all_user) == 0:
        new_user = User(name=user_name, phone=phone, tg_id=id)
        new_booking.aparts.append(select_apart)
        new_user.users_booking.append(new_booking)
        session.add(new_booking, new_user)
        session.commit()




async def get_bookig_list():
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        booking_list = session.query(Booking).join(Apart.apart_name).options(joinedload('*')).all()
    except:
        booking_list = session.query(Booking).options(joinedload('*')).all()
    return booking_list


async def get_free_time_of_room(month, day):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()
    time_list = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00',
                 '11:00',
                 '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00',
                 '23:00']
    busy_time = session.query(Booking.time).where(Booking.month == month and Booking.day == day).all()
    for time in busy_time:
        time_list.remove(time[0])
    return time_list


# async def get_user_info(name,phone,id):
#     engine = create_engine(URL.create(**DATABASE))
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     result = []
#     new_user = User(name=name, phone=phone, tg_id=id)
#     new_booking = Booking(month=month, time=time, day=day)
#     new_booking.aparts.append(select_apart)
#     session.add(new_booking)
#     session.commit()




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

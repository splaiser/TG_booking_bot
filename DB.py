from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from config import DATABASE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):  # Таблица с клиентами где хранятся Ники, телефоны, Телеграмм идентефикаторы
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(30))
    phone = Column(String)
    tg_ident = Column(String)


class Apart(Base):  # Таблица где хранятся Название номера, цена
    __tablename__ = "Apart"

    apart_id = Column(Integer, primary_key=True)
    apart_name = Column(String)
    apart_price = Column(Integer)
    aparts_photo = relationship("Apart_photo", backref="apart")
    booking = relationship("Booking", secondary="apart_boking")


class Apart_photo(Base):  # Таблица где хранятся ссылки на фотографии номеров отеля
    __tablename__ = "Apart_photo"

    photo_id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    apart_id = Column(Integer, ForeignKey(Apart.apart_id))


class Booking(Base):  # Таблица где сохраняются время и дата брони
    __tablename__ = "Booking"

    booking_id = Column(Integer, primary_key=True)
    time = Column(Time)
    date = Column(Date)
    aparts = relationship("Apart", secondary="apart_boking")


apart_boking = Table(
    "apart_boking", Base.metadata,
    Column('apart_id', Integer, ForeignKey(Apart.apart_id)),
    Column('booking_id', Integer, ForeignKey(Booking.booking_id)),
)


def create_db():  # Создаёт таблицы в БД
    engine = create_engine(URL.create(**DATABASE))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


def add_apartment(apart_name, apart_price, apart_photo):
    engine = create_engine(URL.create(**DATABASE))
    Session = sessionmaker(bind=engine)
    session = Session()

    new_apart = Apart(apart_name=apart_name, apart_price=apart_price)

    session.add(new_apart)
    session.commit()


def add_apartment_photo(apart_photo_url):
    pass


def get_last_order():
    pass


def get_user_info(chat_id, user_name, user_phone=""):
    pass


if __name__ == "__main__":
    # create_db()
    add_apartment("test", "20000", "apartment_photo/1.jpg")

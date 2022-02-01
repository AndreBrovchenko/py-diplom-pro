import sqlalchemy as sq
from name_var import database_name
import enum
from enum import Enum
# import main
# from main import database_name
from pprint import pprint
# from name_var import database_name

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# создается базовый класс с помощью вызова функции
Base = declarative_base()

engine = sq.create_engine(database_name)
Session = sessionmaker(bind=engine)


class EnumRelations(enum.Enum):
    not_specified = 0
    single = 1
    have_a_friend = 2
    engaged = 3
    married = 4
    complicated = 5
    actively_searching = 6
    in_love = 7
    in_a_civil_marriage = 8


class EnumSex(enum.Enum):
    not_specified = 0
    female = 1
    male = 2


# колонки объявляются как атрибуты класса
class Cities(Base):
    __tablename__ = 'cities'
    id_city = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, nullable=False)
    city = sq.Column(sq.String(50), nullable=False, unique=True)
    id_country = sq.Column(sq.Integer, sq.ForeignKey('countries.id_country'))
    country = relationship('Countries', backref='cities')


class Countries(Base):
    __tablename__ = 'countries'
    id_country = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, nullable=False)
    country = sq.Column(sq.String(50), nullable=False, unique=True)


class Users(Base):
    __tablename__ = 'users'
    id_user = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False)
    first_name = sq.Column(sq.String(50), nullable=False, unique=True)
    last_name = sq.Column(sq.String(50), nullable=False, unique=True)
    id_city = sq.Column(sq.Integer, sq.ForeignKey('cities.id_city'))
    city = relationship('Cities', backref='users')
    bdate = sq.Column(sq.String(10), nullable=False, unique=True)
    is_closed = sq.Column(sq.Boolean, nullable=False, unique=True)
    id_relation = sq.Column(sq.Enum(EnumRelations))
    id_sex = sq.Column(sq.Enum(EnumSex))


class Customers(Base):
    __tablename__ = 'customers'
    id_customer = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id_user'))
    user = relationship('Users', backref='customer', uselist=False)
    candidates = relationship('Candidates', secondary='friends', backref='customers')


class Candidates(Base):
    __tablename__ = 'candidates'
    id_candidate = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id_user'))
    user = relationship('Users', backref='candidate', uselist=False)


candidate_to_customer = sq.Table(
    'friends', Base.metadata,
    sq.Column('id_customer', sq.Integer, sq.ForeignKey('customers.id_customer')),
    sq.Column('id_candidate', sq.Integer, sq.ForeignKey('candidates.id_candidate')),
)


class WorkWithDatabaseSQL:
    def __init__(self, database):
        # создаем engine
        # self.engine = sqlalchemy.create_engine(database)
        engine = sq.create_engine(database)
        self.connect = engine.connect()

    # def connect_database(self):
    #     # установим соединение
    #     # return self.engine.connect()
    #     self.connect = self.engine.connect()

    def query_from_database(self, sql_text):
        # return db.connect_database().execute(sql_text).fetchall()
        return self.connect.execute(sql_text).fetchall()


if __name__ == '__main__':
    pass
    # connect_bd()

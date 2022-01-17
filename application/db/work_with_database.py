import sqlalchemy
# import main
# from main import database_name
from pprint import pprint
# from name_var import database_name


class WorkWithDatabase:
    def __init__(self, database):
        # создаем engine
        # self.engine = sqlalchemy.create_engine(database)
        engine = sqlalchemy.create_engine(database)
        self.connect = engine.connect()

    # def connect_database(self):
    #     # установим соединение
    #     # return self.engine.connect()
    #     self.connect = self.engine.connect()

    def query_from_database(self, sql_text):
        # return db.connect_database().execute(sql_text).fetchall()
        return self.connect.execute(sql_text).fetchall()

# def connect_bd():
#     db_name = 'postgresql://user_vkinder:pass_vkinder@localhost:5432/vkinder'
#     db = WorkWithDatabase(db_name)
#     name_field = 'relations'
#     sql_text = f'SELECT * FROM {name_field}'
#     # выберем все поля из таблицы relation
#     # sel = db.connect_databse().execute("""SELECT * FROM relations;
#     #         """).fetchall()
#     sel = db.connect_database().execute(sql_text).fetchall()
#     pprint(sel)
#     for elem in sel:
#         if elem[1] == 3:
#             print(elem)
#             break
#     # print(sel[0][2])


# def find_user(user_id):
#     # db_name = 'postgresql://user_vkinder:pass_vkinder@localhost:5432/vkinder'
#     db = WorkWithDatabase(database_name)
#     sql_text = f'SELECT user_id FROM users WHERE user_id = {user_id}'
#     # выберем все поля из таблицы relation
#     sel = db.connect_database().execute(sql_text).fetchall()
#     pprint(sel)
#     return sel


# def query_from_database(sql_text):
#     db = WorkWithDatabase(database_name)
#     return db.connect_database().execute(sql_text).fetchall()


if __name__ == '__main__':
    pass
    # connect_bd()

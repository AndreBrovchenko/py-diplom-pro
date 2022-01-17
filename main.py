from random import randrange
# Импортируем библиотеку vk_api
import vk_api
# Достаём из неё longpoll
from vk_api.longpoll import VkLongPoll, VkEventType
# from application.db.work_with_database import query_from_database
# from application.db.work_with_database import find_user, query_from_database
from name_var import database_name, token_app, token_group, id_group
from application.db.work_with_database import WorkWithDatabase


import requests
import datetime
from pprint import pprint
# from random import randrange


class VK:
    url = 'https://api.vk.com/method/'

    # нельзя использовать токен группы, только токен пользователя (приложения)
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_people_list(self):
        # upload_url = "https://api.vk.com/method/users.search"
        # headers = self.get_headers()
        # params = {
        #     'age_from': 20,
        #     'age_to': 30,
        #     'sex': 0,
        #     'status': 1,
        #     'hometown': 'Котово',
        #     'fields': 'is_no_index, is_closed, can_access_closed, city, home_town, sex, status, photo, relation'
        # }
        # response = requests.get(url=upload_url, headers=headers, params=params)
        # if response.status_code == 202:
        #     print(f"Файл {file_to_disk} записан на Я.Диск")
        # --------------------------------------------------
        group_search_url = self.url + 'users.search'
        group_search_params = {
            'age_from': 20,
            'age_to': 30,
            'sex': 0,
            'hometown': 'Котово',
            'fields': 'is_no_index, is_closed, can_access_closed, city, home_town, sex, status, photo, relation'
        }
        req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        # --------------------------------------------------
        # pprint(response.json())
        # return response.json()
        # pprint(req['response']['items'])
        return req['response']['items']

    def get_contact_information(self, user_id):
        # можно получить данные о нескольких пользователях, если передать в параметре user_ids несколько user_id разделенных запятыми
        group_search_url = self.url + 'users.get'
        group_search_params = {
            'user_ids': user_id,
            'fields': 'is_closed, can_access_closed, bdate, city, country, first_name_, home_town, last_name_, relation, sex, status, photo'
        }
        req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        # --------------------------------------------------
        # pprint(response.json())
        # return response.json()
        # pprint(req['response']['items'])
        # return req['response']['items']
        return req['response']


class ChatBot:
    # нельзя использовать токен пользователя, только токен группы
    def __init__(self, token):
        # Подключаем r VK_API с помощью токена
        self.vk = vk_api.VkApi(token=token)

    def connect_longpoll(self):
        # Подключаем longpoll
        return VkLongPoll(self.vk)

    # Создадим функцию для ответа на сообщения в лс группы
    def write_msg(self, user_id, message, attachment):
        print(f'ChatBot ответил пользователю {user_id} сообщением: {message}:')
        # vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})
        self.vk.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': randrange(10 ** 7),
        })

    def get_user_get(self, user_id):
        req = self.vk.method('users.get', {
            'user_ids': user_id,
            'fields': 'is_closed, can_access_closed, bdate, city, country, first_name_, '
                      'home_town, last_name_, relation, sex, status, photo, schools'
        })
        return req


def get_tokens():
    pass
    # print(f'Запрашиваем токен от пользователя\n ----')
    # token_vk = input('Введите ТОКЕН: ')
    # token = input('Token: ')


def find_people_matching_conditions():
    # найти людей, соответствующих условиям
    # (начало) - Часть кода для получения списка людей посредством библиотеки request
    # # print(f'Запрашиваем токен от пользователя\n ----')
    # # token_vk = input('Введите ТОКЕН: ')
    # # token = input('Token: ')
    vk_client = VK(token_app, '5.131')
    people_data = vk_client.get_people_list()
    for item in people_data:
        if 'relation' in item:
            print(f"{item['first_name']} {item['last_name']} relation:{item['relation']}")
        else:
            print(f"{item['first_name']} {item['last_name']}")
    # (конец) - Часть кода для получения списка людей посредством библиотеки request


def contact_information(user_id):
    # получить данные собеседника
    vk_client = VK(token_group, '5.131')
    return vk_client.get_contact_information(user_id)


def talk_with_chatbot():
    # поговорить с чат-ботом
    # ----------------------------------------
    # для подключения к VkApi используем только токен группы
    # print(f'Запрашиваем токен группы пользователей VK\n ----')
    # token_group = input('Введите токен группы пользователей VK: ')
    # # Подключаем токен и longpoll ------------
    # vk = vk_api.VkApi(token=token_group)
    chat_bot = ChatBot(token_group)
    # # give = vk.get_api() # (этой строки в примере нетологии не было)
    # print(give.wall.post(message='Hello world!'))
    longpoll = chat_bot.connect_longpoll()
    # longpoll = VkLongPoll(vk, group_id=209987730)
    # longpoll = VkLongPoll(vk, id_group)
    # # ------------
    # Слушаем longpoll(Сообщения)
    # talk_mode = 0
    # user_id_old = ''
    # user_id_new = ''
    db = WorkWithDatabase(database_name)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_me:
                print('ChatBot ответил пользователю')
            # Чтобы наш бот не слышал и не отвечал на самого себя
            if event.to_me:
                # Для того чтобы бот читал все с маленьких букв
                request = event.text.lower()
                # Для того чтобы бот читал
                # request = event.text
                # Получаем id пользователя (этой строки в примере нетологии не было)
                user_id = event.user_id
                # хотелл отказаться от того, чтобы каждый раз выяснять id пользователя.
                # Оказывается это нужно делать каждый раз, потому что бот может общаться
                # одновременно с несколькими пользователями
                # if user_id == user_id_old:
                #     print('пользователь тот же')
                # else:
                #     user_id_old = user_id
                #     print('другой пользователь')
                # contact = VK(token_group, '5.131')
                # fio = contact.get_contact_information(user_id)
                # fio = contact_information(user_id)
                # структура данных пользователя по умолчанию (со всеми полями)
                user_data = {
                    'is_closed': False,
                    'can_access_closed': False,
                    'bdate': '',
                    'city': -1,
                    'country': -1,
                    'first_name': '',
                    'home_town': '',
                    'last_name': '',
                    'relation': -1,
                    'sex': -1,
                    'status': '',
                    'photo': '',
                    'schools': []
                }
                # данные пользователя полученные с VK
                user = chat_bot.get_user_get(user_id)[0]
                # user_new = user[0]
                # бывает что в запросе не все поля, в этом случае возникает ошибка 'KeyError'
                # user_data = {
                #     'is_closed': user[0]['is_closed'],
                #     'can_access_closed': user[0]['can_access_closed'],
                #     'bdate': user[0]['bdate'],
                #     'city': user[0]['city'],
                #     'country': user[0]['country'],
                #     'first_name_': user[0]['first_name_'],
                #     'home_town': user[0]['home_town'],
                #     'last_name': user[0]['last_name'],
                #     'relation': user[0]['relation'],
                #     'sex': user[0]['sex'],
                #     'status': user[0]['status'],
                #     'photo': user[0]['photo'],
                #     'schools': user[0]['schools']
                # }
                # обновляем словарь user_data словарем user
                # обновляем данные по умолчанию с полученными с VK данными
                user_data.update(user)
                # теперь надо обратиться к БД и выяснить, нет ли уже в ней данного пользователя
                # если нет то добавить, если есть, посмотреть полноту данных о пользователе.
                sql_text = f'SELECT id_user, user_id FROM users WHERE user_id = {user_id}'
                user_db = db.query_from_database(sql_text)
                # user_db = query_from_database(sql_text)
                # проба получить единственную запись из таблицы и взять значение ее поля id
                sql_text = f'SELECT * FROM relations WHERE id = 3'
                # q = query_from_database(sql_text)
                # q = db.query_from_database(sql_text)
                # если мы получаем данные из таблицы БД, то это список кортежей
                # получить элемент кортежа можно указав индекс кортежа, а затем если нужно индекс элемента кортежа
                # например query[0][0]
                # print(f'id_user: {q[0][0]}')
                if len(user_db) > 0:
                    print('пользователь найден в базе')
                    # нужно выяснить значение поля user_id
                    field_user_id = user_db[0][0]
                    print(f'id_user: {field_user_id}')
                    # теперь нужно проверить нет ли его в базе customers, если нет, добавить, иначе ничего не делать
                    # print(f'id_user: {user_db[0]}')
                    sql_text = f'SELECT * FROM customers WHERE id_user = {field_user_id}'
                    user_customer = db.query_from_database(sql_text)
                    if len(user_customer) > 0:
                        # пользователь уже обращался для поиска пары. Ничего не делаем
                        pass
                    else:
                        # пользователь НЕ обращался для поиска пары. Добавляем его в таблицу customers
                        pass
                    # pprint(query_from_database(sql_text))
                else:
                    print('пользователя нет в базе')
                    # его нужно добавить в таблицу users и таблицу customers
                pprint(user_data)
                # pprint(user_data[0])
                # print(user[0]['first_name'])
                print(f"{user_data['first_name']} {user_data['last_name']}, семейное положение "
                      f"{user_data['relation']} , пол {user_data['sex']} ")
                # print(fio)
                # print(contact)
                # print(f'Пользователь {user_id} написал: {request}', 'attachment')
                # print(f"Пользователь {user_data[0]['first_name']} написал: {request}")
                print(f"Пользователь {user_data['first_name']} написал: {request}")
                # if talk_mode == 0:
                #     print('режим 0')
                # elif talk_mode == 1:
                #     print('режим 1')
                #     talk_mode = 0
                if request == "привет":
                    # chat_bot.write_msg(user_id, f"Хай, {user_id}", 'attachment')
                    message = f"Привет, {user_data['first_name']}\n" \
                              f"Я ЧатБот для знакомств. Могу найти Вам пару\n" \
                              f"Если хотите, напишите мне 'знакомство'"
                    chat_bot.write_msg(user_id, message, 'attachment')
                    # f = chat_bot.get_user_search(user_id)
                elif request == 'знакомство':
                    message = f"Я предлагаю следующие критерии поиска пары:\n" \
                              f"возраст: "
                    # talk_mode = 1
                elif request == "пока":
                    chat_bot.write_msg(user_id, "Пока((", 'attachment')
                    # break
                elif request == 'картинка':
                    # Отправляем картинку и текст (этого блока в примере нетологии не было)
                    chat_bot.vk.method("messages.send", {
                        "peer_id": user_id,
                        "message": "Вот твоя картинка!",
                        "attachment": "photo381260583_457370887",
                        "random_id": 0
                    })
                else:
                    chat_bot.write_msg(user_id, "Не поняла вашего ответа...", 'attachment')


def main():
    talk_with_chatbot()


if __name__ == '__main__':
    main()
    # connect_bd()
    # find_user(1)

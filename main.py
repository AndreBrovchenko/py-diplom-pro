from random import randrange
# Импортируем библиотеку vk_api
import vk_api
# Достаём из неё longpoll
from vk_api.longpoll import VkLongPoll, VkEventType
# from application.db.work_with_database import query_from_database
# from application.db.work_with_database import find_user, query_from_database
from application.db.work_with_database import Base, engine, Session
from application.db.work_with_database import Cities, Users, Customers, Candidates, EnumRelations, EnumSex # , Countries, Relations, Sex, Friends
from name_var import database_name, token_app, token_group, id_group
from application.db.work_with_database import WorkWithDatabaseSQL


import requests
import datetime
from pprint import pprint
# from random import randrange


class VK:
    url = 'https://api.vk.com/method/'
    try:
        pass
    except requests.HTTPError as err:
        code = err.response.status_code
        print(f'Код ошибки: {code}')
    else:
        # Отработает если у нас нет исключений
        # print("Все прошло успешно исключений нет")
        pass
    finally:
        pass

    # нельзя использовать токен группы, только токен пользователя (приложения)
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_cities(self, city, region):
        group_search_url = self.url + 'database.getCities'
        group_search_params = {
            'q': city,
            'country_id': 1,
            'count': 100
        }
        # req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        response = requests.get(url=group_search_url, params={**self.params, **group_search_params})
        req = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            for item in req['response']['items']:
                _region = item['region'].split(' ')[0].lower()
                if item['title'].lower() == city.lower() and _region == region.lower():
                    return item['id']

    def get_people_list(self, find_param):
        group_search_url = self.url + 'users.search'
        group_search_params = {
            'age_from': find_param['возраст от'],
            'age_to': find_param['возраст до'],
            'sex': find_param['пол'],
            'city': find_param['город'],
            'relation': find_param['семейное положение'],
            'fields': 'is_no_index, is_closed, can_access_closed, city, home_town, sex, status, photo, relation'
        }
        # req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        response = requests.get(url=group_search_url, params={**self.params, **group_search_params})
        req = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            return req['response']['items']

    def get_user_get(self, user_ids):
        # 'https://vk.com/' + domain
        # friend_status <> 3
        # has_photo == 1
        # is_friend == 0
        group_search_url = self.url + 'users.get'
        group_search_params = {
            'user_ids': user_ids,
            'fields': 'is_closed, domain, friend_status, has_photo, is_friend, screen_name, site, photo, relation'
        }
        # req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        response = requests.get(url=group_search_url, params={**self.params, **group_search_params})
        req = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            return req['response']['items']

    def photos_get(self, album, ext=0, owner_id=None):
        """
        Параметры album_id (идентификатор альбома)
        wall — фотографии со стены;
        profile — фотографии профиля;
        saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        Параметры extended
        0 - по умолчанию - дополнительные поля не возвращаются
        1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts.
        """
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'album_id': album,
            'extended': ext,
            'owner_id': owner_id
        }
        # req = requests.get(url=photos_get_url, params={**self.params, **photos_get_params}).json()
        response = requests.get(url=photos_get_url, params={**self.params, **photos_get_params})
        req = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            return req['response']['items']

    def get_contact_information(self, user_id):
        # можно получить данные о нескольких пользователях,
        # если передать в параметре user_ids несколько user_id разделенных запятыми
        group_search_url = self.url + 'users.get'
        group_search_params = {
            'user_ids': user_id,
            'fields': 'is_closed, can_access_closed, bdate, city, country, '
                      'first_name_, home_town, last_name_, relation, sex, status, photo'
        }
        # req = requests.get(url=group_search_url, params={**self.params, **group_search_params}).json()
        response = requests.get(url=group_search_url, params={**self.params, **group_search_params})
        req = response.json()
        response.raise_for_status()
        if response.status_code == 200:
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
        print(f'ChatBot сейчас ответит пользователю {user_id} сообщением:\n{message}:')
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


vk_client = VK(token_app, '5.131')
db = WorkWithDatabaseSQL(database_name)
session = Session()

# структура данных пользователя по умолчанию (со всеми полями)
user_data_master = {
    'is_closed': False,
    'can_access_closed': False,
    'bdate': '',
    'city': -1,
    'country': -1,
    'first_name': '',
    'home_town': '',
    'last_name': '',
    'relation': 0,
    'sex': 0,
    'status': '',
    'photo': '',
    'schools': []
}


sex_list = {0: 'не указано', 1: 'женский', 2: 'мужской'}
relation_list = {
    0: 'не указано',
    1: 'не женат/не замужем',
    2: 'есть друг/есть подруга',
    3: 'помолвлен/помолвлена',
    4: 'женат/замужем',
    5: 'всё сложно',
    6: 'в активном поиске',
    7: 'влюблён/влюблена',
    8: 'в гражданском браке',
}


def create_message_help(recipient):
    return f"/{recipient} возраст 25\n" \
           f"{recipient} пол n\n" \
           f"   где n, это одно из значений:\n" \
           f"   1 - женский;\n" \
           f"   2 - мужской;\n" \
           f"/{recipient} город Город\n" \
           f"/{recipient} с_п n\n где n\n" \
           f" {recipient} n, это одно из значений:\n" \
           f"   1 - не женат/не замужем;\n" \
           f"   2 - есть друг/есть подруга;\n" \
           f"   3 - помолвлен/помолвлена;\n" \
           f"   4 - женат/замужем;\n" \
           f"   5 - всё сложно;\n" \
           f"   6 - в активном поиске;\n" \
           f"   7 - влюблён/влюблена;\n" \
           f"   8 - в гражданском браке;\n"


def create_message_help_new():
    return f"Для ввода критериев поиска введи строку:\n" \
           f"/найди возраст_от возраст_до пол город регион семейное_положение\n" \
           f"   например: /найди 25 30 1 Москва Московская 6\n" \
           f"   --------------------------\n" \
           f"   варианты пол\n" \
           f"   1 - женский;\n" \
           f"   2 - мужской;\n" \
           f"   варианты С_П\n" \
           f"   1 - не женат/не замужем;\n" \
           f"   2 - есть друг/есть подруга;\n" \
           f"   3 - помолвлен/помолвлена;\n" \
           f"   4 - женат/замужем;\n" \
           f"   5 - всё сложно;\n" \
           f"   6 - в активном поиске;\n" \
           f"   7 - влюблён/влюблена;\n" \
           f"   8 - в гражданском браке;\n"


def command_processing():
    pass


def find_user_in_db_sql(user_id):
    sql_text = f'SELECT id_user, user_id FROM users WHERE user_id = {user_id}'
    table_users = db.query_from_database(sql_text)
    if len(table_users) > 0:
        # print('пользователь найден в базе')
        # нужно выяснить значение поля user_id
        id_user_in_users = table_users[0][0]
        print(f'id_user: {id_user_in_users}')
        # теперь нужно проверить нет ли его в базе customers, если нет, добавить, иначе ничего не делать
        # print(f'id_user: {user_db[0]}')
        sql_text = f'SELECT * FROM customers WHERE id_user = {id_user_in_users}'
        table_customers = db.query_from_database(sql_text)
        if len(table_customers) == 0:
            # пользователь НЕ обращался для поиска пары. Добавляем его в таблицу customers
            pass
        # pprint(query_from_database(sql_text))
    else:
        pass
        # print('пользователя нет в базе')
        # его нужно добавить в таблицу users и таблицу customers


def find_user_in_table_users_orm(user_id):
    # !!! эту функцию не использую. Ее роль выполняет функция added_user_orm
    users = session.query(Users).filter(Users.user_id == user_id).first()
    if users is not None:
        print(f'+пользователь {user_id} найден в базе пользователей')
        return True
    else:
        print(f'+пользователя {user_id} нет в базе пользователей')
        # нужно проверить полноту данных о пользователе и при необходимости запросить отсутствующие
        return False


def added_customer_orm(id_user, user_id):
    # теперь нужно проверить нет ли его в базе customers, если нет, добавить, иначе ничего не делать
    user_in_customer = session.query(Customers).join(
        Users, Users.id_user == Customers.id_user).filter(
        Users.user_id == user_id).first()
    # print(user_in_customer)
    if user_in_customer is None:
        # print(f'+пользователя {user_id} нет в базе customers')
        # new_user = Users(id_user=users.id_user)
        new_customer = Customers(id_user=id_user)
        session.add(new_customer)
        session.commit()
        # print(f'+пользователь {user_id} добавлен в базу customers')
        return new_customer.id_customer
    else:
        return user_in_customer.id_customer


def find_candidate_orm(id_user, user_id):
    # ищет человека в таблице candidates с привязкой к пользователю
    user_in_candidate = session.query(Users).join(
            Candidates, Users.id_user == Candidates.id_user).filter(
            Users.user_id == user_id).first()
    if user_in_candidate is None:
        # print(f'+пользователя {user_id} нет в базе кандидатов')
        # new_user = Users(id_user=users.id_user)
        new_customer = Customers(id_user=id_user)
        session.add(new_customer)
        session.commit()
        print(f'+пользователь {user_id} добавлен в базу кандидатов')


def added_user_orm(user_id, user_data):
    # параметр user_id можно не передавать, его можно получить из user_data['id']
    s = user_data['id']
    user = session.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        # print(f'+пользователь {user_id} НЕ найден в базе пользователей')
        # его нужно добавить в таблицу users и таблицу customers
        # relation = relation_list_enum[user_data['relation']]
        # sex = relation_list_enum[user_data['sex']]
        new_user = Users(user_id=user_data['id'],
                         first_name=user_data['first_name'],
                         last_name=user_data['last_name'],
                         id_city=user_data['city'],
                         bdate=user_data['bdate'],
                         is_closed=user_data['is_closed'],
                         id_relation=EnumRelations(user_data['relation']).name,
                         id_sex=EnumSex(user_data['sex']).name,
                         )
        # id_relation = EnumRelations(user_data['relation']).value,
        session.add(new_user)
        # после добавления пользователя, нужно сделать commit() потому что пока запись не внесена в
        # таблицу, у нее нет id, и в связанной таблице вместо значения id будет NULL
        session.commit()
        return new_user.id_user
    else:
        # print(f'+пользователь {user_id} найден в базе пользователей')
        return user.id_user


def check_completed_data_user(user_data):
    # Начинаем уточнять данные пользователя
    # Известна ли дата рождения, чтобы выяснить возраст
    # Возвращается в формате D.M.YYYY или D.M (если год рождения скрыт)
    bdate = user_data['bdate']
    if len(bdate) == 0:
        # дата рождения не указана
        print('Укажите дату рождения')
    elif len(bdate) < 6:
        # год рождения скрыт
        print('Вы не указали год рождения')
    else:
        year_date = bdate[-4:]
        if year_date.isdigit():
            print(year_date)
        else:
            print('Год должен состоять из цифр. Повторите ввод года')
    # Известен ли пол
    sex = user_data['sex']
    # Известен ли город
    city = user_data['city']
    # Известно ли семейное положение
    relation = user_data['relation']
    # Начинаем уточнять критерии поиска пары

    # Выбираем подходящие кандидатуры
    pass


def get_search_parameters(argument):
    key = ['возраст от', 'возраст до', 'пол', 'город', 'регион', 'семейное положение']
    # создаем словарь из двух списков
    find_param = {k: v for k, v in zip(key, argument)}
    # "Вы ввели следующие критерии поиска. Начинаю поиск." (добавить эти фразы в сообщение
    find_msg = ''
    for k, v in find_param.items():
        if k == 'пол':
            msg = sex_list[int(v)]
            find_msg = find_msg + f'{k}: {msg}\n'
        elif k == 'семейное положение':
            msg = relation_list[int(v)]
            find_msg = find_msg + f'{k}: {msg}\n'
        else:
            find_msg += f'{k}: {v}\n'
    find_param['возраст от'] = int(find_param['возраст от'])
    find_param['возраст до'] = int(find_param['возраст до'])
    find_param['пол'] = int(find_param['пол'])
    id_city = vk_client.get_cities(find_param['город'], find_param['регион'])
    find_param['город'] = id_city
    find_param['семейное положение'] = int(find_param['семейное положение'])
    return find_msg, find_param


def candidate_list_processing(user_id, user_chat, find_param):
    # функция обработки списка кандидатов
    # теперь нужно выбрать людей по критериям,
    people_data = vk_client.get_people_list(find_param)
    # получим id_user заказчика
    id_user = added_user_orm(user_id, user_chat)
    # проверить есть ли заказчик в таблице customers
    id_customer = added_customer_orm(id_user, user_id)
    # брать по одному, проверить не отправляли ли мы его пользователю ранее, если нет, то отправить и выйти из цикла
    for item in people_data:
        if item['is_closed']:
            # профиль скрыт настройками приватности, мы не сможем получить нужную нам информацию
            # к тому же кандидат уже является другом пользователя "or item['friend_status'] == 3"
            continue
        # проходим по списку найденных кандидатур, проверяем нет ли человека в базе users
        # затем проверяем не был ли он кандидатом для заказчика,
        # если не был, то добавляем его в таблицу candidates для данного customers-а
        # и отправляем заказчику данные на кандидата.
        # Выходим из цикла
        user_people = user_data_master.copy()
        # обновляем словарь user_people (данные по умолчанию) словарем item (полученными с VK)
        user_people.update(item)
        candidate_user_id = item['id']
        # print(f"candidate_user_id: {candidate_user_id}")
        # если кандидатуры не было в базе пользователей, то он будет добавлен и вернется валидный candidate_id_user
        # candidate_user_id можно получить из user_people.item['id']. Поэтому можно передавать один параметр
        candidate_id_user = added_user_orm(candidate_user_id, user_people)
        # теперь надо проверить не отправляли ли данного кандидата данному customer-у.
        # Если не отправляли, то его надо "привязать" к customer-у и отправить customer-у его данные
        # subq = session.query(Customers).filter(Customers.id_user == id_user).subquery()
        # q = session.query(Candidates).join(subq, Candidates.id_candidate == subq.c.id_customer).first()
        # response = session.query(Customers).filter_by(id_user=id_user).first().candidates
        response = session.query(Customers).filter_by(id_customer=id_customer).first().candidates
        # -------------------------------
        # exist_candidate = session.query(Candidates).join(Customers).\
        #     filter_by(id_user=candidate_id_user).\
        #     filter(Customers.id_user == id_customer).first()
        # if exist_candidate is not None:
        #     return "Новый пользователь уже среди кандидатов"
        # -------------------------------
        no_find_flag = True
        for item_candidate in response:
            if item_candidate.id_user == candidate_id_user:
                no_find_flag = False
                break
        # if q is None:
        if no_find_flag:
            adding_customers_and_candidates(user_id, id_customer, candidate_id_user)
            candidate_user_url = 'https://vk.com/id' + str(candidate_user_id)
            tuple_photos = photo_list_processing(candidate_user_id)
            msg_attachment = ''
            for item_attach in tuple_photos:
                msg_attachment += f"photo{item_attach[3]}_{item_attach[2]},"
            msg_attachment = msg_attachment.rstrip(',')
            return candidate_user_url, msg_attachment
    # то получить 3 популярных фотографии профиля,
    # добавить его в таблицу users и таблицу candidates
    # и отправить их пользователю вместе со ссылкой на найденного человека


def adding_customers_and_candidates(user_id, id_customer, candidate_id_user):
    # добавление заказчиков и кандидатов
    current_user = session.query(Users).filter(Users.user_id == user_id).first()
    customer = session.query(Customers).filter(Customers.id_customer == id_customer).first()
    candidate = session.query(Candidates).filter(Candidates.id_user == candidate_id_user).first()
    if candidate is None:
        candidate = Candidates(id_user=candidate_id_user)
        session.add(candidate)
        # Используем flush, чтобы получить id категории, которая будет добавлена
        session.flush()
    # Добавим связь
    customer.candidates.append(candidate)
    session.add(customer)
    session.commit()


def photo_list_processing(candidate_user_id):
    # обработка списка фотографий
    list_photos_vk = vk_client.photos_get('profile', 1, candidate_user_id)
    list_photos = []
    for item_photo in list_photos_vk:
        print(f"лайки: {item_photo['likes']['count']}, комментарии: {item_photo['comments']['count']}")
        for item_sizes in item_photo['sizes']:
            # type = m — Пропорциональная копия изображения с максимальной стороной 130px;
            print(
                f"{item_sizes['type']} - {item_sizes['height']} - {item_sizes['width']} - {item_sizes['url']}")
            if item_sizes['type'] == 'm' and item_sizes['url'][-4:] == '.jpg':
                new_tuple = (item_photo['likes']['count'],
                             item_sizes['url'],
                             item_photo['id'],
                             item_photo['owner_id'])
                list_photos.append(new_tuple)
    temp_photos = tuple(list_photos)
    temp_photos = tuple(sorted(temp_photos))
    tuple_photos = temp_photos[:-4:-1]
    return tuple_photos


def talk_with_chatbot():
    # поговорить с чат-ботом
    # для подключения к VkApi используем только токен группы
    # # Подключаем токен и longpoll ------------
    chat_bot = ChatBot(token_group)
    longpoll = chat_bot.connect_longpoll()
    # longpoll.session.
    # Слушаем longpoll(Сообщения)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_me:
                # print(f'ChatBot ответил пользователю:\n{event.text}')
                pass
            # Чтобы наш бот не слышал и не отвечал на самого себя
            if event.to_me:
                # Для того чтобы бот читал все с маленьких букв
                request = event.text.lower()
                # пользователь обратился к боту, для продолжения беседы, нужно немного узнать о нем
                # Получаем id пользователя (этой строки в примере нетологии не было)
                user_id = event.user_id
                # бывает что в запросе не все поля, в этом случае возникает ошибка 'KeyError'
                # данные пользователя полученные с VK
                user = chat_bot.get_user_get(user_id)[0]
                user_chat = user_data_master.copy()
                # обновляем словарь user_chat словарем user (данные по умолчанию с полученными с VK данными)
                user_chat.update(user)
                # pprint(user_chat)
                # print(f"Пользователь {user_chat['first_name']} написал: {request}")
                # теперь надо обратиться к БД и выяснить, нет ли уже в ней данного пользователя
                # если нет то добавить, если есть, посмотреть полноту данных о пользователе.
                # ищем в базе пользователя
                if request[0] == '/':
                    input_msg = request[1:].split(' ')
                    print('вошли в обработку команд')
                    command = input_msg[0]
                    argument = input_msg[1:]
                    if command == 'знакомство':
                        # пользователь решил искать пару, проверим нет ли его в базе (может он уже обращался к боту)
                        # если его в базе нет, проверить полноту его данных и запросить у пользователя недостающие
                        # после получения всех данных, внести его в базу
                        # нужно иметь ввиду что в эту часть мы попадем только если пользователь наберет "/знакомство"
                        # а когда мы начнем уточнть данные о пользователе, мы сюда не попадаем.
                        # ищем в базе пользователя
                        # if not find_user_in_table_users_orm(user_id):
                        #     # check_completed_data_user()
                        #     id_user = added_user_orm(user_id)
                        id_user = added_user_orm(user_id, user_chat)
                        added_customer_orm(id_user, user_id)
                        message = create_message_help_new()
                        chat_bot.write_msg(user_id, message, 'attachment')
                    elif command == 'мой':
                        # обработка команд получения данных о пользователе
                        print('# обработка команд получние данных о пользователе')
                        # elif argument[0] == 'возраст':
                        #     print('получаем возраст пользователя')
                        # elif argument[0] == 'пол':
                        #     print('получаем пол пользователя')
                        # elif argument[0] == 'город':
                        #     print('получаем город пользователя')
                        # elif argument[0] == 'с_п':
                        #     print('получаем семейное положение пользователя')
                    elif command == 'найди':
                        # обработка команд критерии поиска
                        print('# обработка команд критериев поиска')
                        if argument[0] == '?':
                            print('# выводим список команд получения данных о пользователе')
                            message = create_message_help_new()
                            chat_bot.write_msg(user_id, message, 'attachment')
                        else:
                            if len(argument) == 6:
                                if argument[0].isdigit() and argument[1].isdigit() and \
                                        argument[2].isdigit() and argument[5].isdigit():
                                    find_msg, find_param = get_search_parameters(argument)
                                    # пишем список параметров которые мы приняли
                                    chat_bot.write_msg(user_id, find_msg, 'attachment')
                                    message, msg_attach = candidate_list_processing(user_id, user_chat, find_param)
                                    chat_bot.write_msg(user_id, message, msg_attach)
                                else:
                                    message = f'Последовательность параметров нарушена, повторите ввод'
                                    chat_bot.write_msg(user_id, message, 'attachment')
                            else:
                                message = f'Вы ввели не все параметры, повторите ввод'
                                chat_bot.write_msg(user_id, message, 'attachment')
                    # chat_bot.write_msg(user_id, "вошли в обработку команд", 'attachment')
                elif request == "привет":
                    message = f"Привет, {user_chat['first_name']}\n" \
                              f"Я ЧатБот для знакомств. Могу найти Вам пару\n" \
                              f"Если хотите, напишите мне '/знакомство'"
                    chat_bot.write_msg(user_id, message, 'attachment')
                    # f = chat_bot.get_user_search(user_id)
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
                    chat_bot.write_msg(user_id, "Не понял вашего ответа...", 'attachment')


def main():
    talk_with_chatbot()


if __name__ == '__main__':
    main()

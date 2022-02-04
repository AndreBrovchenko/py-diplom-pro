-- # входим в режим управления от пользователя postgres (БД тоже postgres)
psql -U postgres	
-- # создаем БД с именем vkinder
create database vkinder;
-- # создаем пользователя с именем <user_vkinder> и паролем <pass_vkinder>
create user user_vkinder with password 'pass_vkinder';
-- # указываем, что владельцем БД <vkinder>
-- # является пользователь <user_ vkinder>
alter database vkinder owner to user_vkinder;
-- # -----------------
-- # входим в режим управления от пользователя user_vkinder (БД vkinder)
psql -U user_vkinder vkinder
-- # -----------------
create table countries (
id_country serial primary key,
id integer not null,
country varchar(50) not null 
);
-- # -----------------
create table cities (
id_city serial primary key,
id integer not null,
city varchar(50) not null,
id_country integer references countries (id_country)
);
-- # -----------------
create table users (
id_user serial primary key,
user_id integer not null,
first_name varchar(50) not null,
last_name varchar(50),
id_city integer references cities (id_city),
bdate varchar(10),
is_closed boolean,
id_relation varchar(30),
id_sex varchar(30)
);
-- # -----------------
create table customers (
id_customer serial primary key,
id_user integer references users (id_user)
);
-- # -----------------
create table candidates (
id_candidate serial primary key,
id_user integer references users (id_user)
);
-- # -----------------
create table friends (
id_friend serial primary key,
id_customer integer references customers (id_customer),
id_candidate integer references candidates (id_candidate)
);
-- # -----------------

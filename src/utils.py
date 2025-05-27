import os

import psycopg2
from dotenv import load_dotenv

from src.api_module import EMPLOYER_IDS, insert_employers, insert_vacancies

load_dotenv()


def create_db(self_dict: dict, dbname: str) -> None:
    """ Функция принимает словарь с параметрами для подключения к базе данных и имя базы данных.
    Создает базу данных с использованием полученных параметров """

    conn = psycopg2.connect(**self_dict)
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS ' + dbname)
        cursor.execute("CREATE DATABASE " + dbname)

    conn.close()


def create_tables(self_dict: dict, dbname: str) -> None:
    """ Функция принимает словарь с параметрами для подключения к базе данных и имя базы данных.
    Создает таблицы базы данных """

    conn = psycopg2.connect(**self_dict, database=dbname)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS vacancies")
    cur.execute("DROP TABLE IF EXISTS employers")
    cur.execute("CREATE TABLE employers (employers_id int PRIMARY KEY, \
                employers_name varchar(150) NOT NULL, \
                number_of_vacancies int)")
    cur.execute("CREATE TABLE vacancies (url varchar(150) PRIMARY KEY, \
                vacancies_name varchar(150) NOT NULL, \
                salary int, \
                employers_id int REFERENCES employers(employers_id) NOT NULL)")

    conn.commit()

    cur.close()
    conn.close()


def load_employers_to_db(data_list: list, self_dict: dict) -> None:
    """ Функция загружает данные о работодателях в базу данных PostgresQL в таблицу employers """
    conn = psycopg2.connect(**self_dict, database='hh_info')
    conn.autocommit = True
    with conn.cursor() as cursor:
        for data in data_list:
            cursor.execute("""INSERT INTO employers (employers_id, employers_name, number_of_vacancies) \
                            VALUES (%s, %s, %s);""",
                           (data['employers_id'],
                            data['employers_name'],
                            data['number_of_vacancies']))

    conn.close()


def load_vacancies_to_db(data_list: list, self_dict: dict) -> None:
    """ Функция загружает данные о вакансиях в базу данных PostgresQL в таблицу vacancies """
    conn = psycopg2.connect(**self_dict, database='hh_info')
    conn.autocommit = True
    with conn.cursor() as cursor:
        for data in data_list:
            cursor.execute("""INSERT INTO vacancies (url, vacancies_name, salary, employers_id) \
                            VALUES (%s, %s, %s, %s);""",
                           (data['url'],
                            data['vacancies_name'],
                            data['salary'],
                            data['employers_id']))

    conn.close()


if __name__ == '__main__':
    dict_data = {
        'host': os.getenv('host'),
        'user':  os.getenv('user'),
        'password': os.getenv('password'),
        'port': os.getenv('port')
    }

    create_db(dict_data, 'hh_info')
    create_tables(dict_data, 'hh_info')

    data_list = insert_employers(EMPLOYER_IDS)
    data_list_1 = insert_vacancies(EMPLOYER_IDS)
    load_employers_to_db(data_list, dict_data)
    load_vacancies_to_db(data_list_1, dict_data)

    conn = psycopg2.connect(**dict_data, database='hh_info')
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers")
    print(cur.fetchall())
    cur.execute("SELECT * FROM vacancies")
    print(cur.fetchall())

    cur.close()
    conn.close()

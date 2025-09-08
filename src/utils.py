import psycopg2
from dotenv import load_dotenv


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

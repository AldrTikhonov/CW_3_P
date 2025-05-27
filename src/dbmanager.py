import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """ """

    def __init__(self, dict_data):

        self.conn = psycopg2.connect(**dict_data, database='hh_info')

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """
        with self.conn.cursor() as cur:

            cur.execute('SELECT DISTINCT employers_name, number_of_vacancies FROM employers JOIN \
            vacancies USING(employers_id)')

            results = cur.fetchall()

            for result in results:

                print(f'Компания: {result[0]}, количество вакансий: {result[1]}')
                print('_____________________________________________________________________')

        self.conn.close()

    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании, названия вакансии,
         зарплаты и ссылки на вакансию """
        with self.conn.cursor() as cur:

            cur.execute('SELECT url, vacancies_name, salary, employers.employers_name \
            FROM vacancies JOIN employers USING(employers_id)')

            results = cur.fetchall()

            for result in results:
                if result[2] == 0:
                    salary = 'Зарплате не указана'
                else:
                    salary = result[2]
                print(f'Компания: {result[-1]}, название вакансии: {result[1]}, зарплата: {salary}, \
ссылки на вакансию: {result[0]}')
                print('_____________________________________________________________________')

        self.conn.close()

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям """
        with self.conn.cursor() as cur:

            cur.execute('SELECT AVG(salary) FROM vacancies')
            results = cur.fetchall()
            for result in results:
                print(f'Средняя зарплата: {round(float(result[0]), 2)}')
                print('___________________________________________________________')

        self.conn.close()

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """

        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
            results = cur.fetchall()
            for result in results:
                print(f'Название вакансии: {result[1]}, Зарплата: {result[2]}, Ссылка: {result[0]}')
                print('_____________________________________________________________________')

        self.conn.close()

    def get_vacancies_with_keyword(self, search_word):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies WHERE vacancies_name ILIKE '%" + search_word + "%'")
            results = cur.fetchall()
            for result in results:
                if result[2] == 0:
                    salary = "Зарплата не указана"
                else:
                    salary = result[2]
                print(f'Название вакансии: {result[1]}, Зарплата: {salary}, Ссылка: {result[0]}')
                print('_____________________________________________________________________')

        self.conn.close()


if __name__ == '__main__':
    dict_data = {
        'host': os.getenv('host'),
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'port': os.getenv('port')
    }

    a = DBManager(dict_data)
    # a.get_all_vacancies()
    # a.get_companies_and_vacancies_count()
    # a.get_avg_salary()
    # a.get_vacancies_with_higher_salary()
    a.get_vacancies_with_keyword('Специалист')

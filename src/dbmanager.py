import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """ Класс для работы с базой данных PostgresQL, содержащей информацию о работодателях и вакансиях"""

    def __init__(self, dict_data: dict):

        self.conn = psycopg2.connect(**dict_data, database='hh_info')
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> None:
        """ Получает список всех компаний и количество вакансий у каждой компании """
        self.cur.execute('SELECT DISTINCT employers_name, number_of_vacancies FROM employers JOIN \
        vacancies USING(employers_id)')

        results = self.cur.fetchall()

        for result in results:
            print(f'Компания: {result[0]}, количество вакансий: {result[1]}')
            print('_____________________________________________________________________')

    def get_all_vacancies(self) -> None:
        """ Получает список всех вакансий с указанием названия компании, названия вакансии,
         зарплаты и ссылки на вакансию """
        self.cur.execute('SELECT url, vacancies_name, salary, employers.employers_name \
        FROM vacancies JOIN employers USING(employers_id)')

        results = self.cur.fetchall()

        for result in results:
            if result[2] == 0:
                salary = 'Зарплате не указана'
            else:
                salary = result[2]
            print(f'Компания: {result[-1]}, название вакансии: {result[1]}, зарплата: {salary}, \
ссылки на вакансию: {result[0]}')
            print('_____________________________________________________________________')

    def get_avg_salary(self) -> None:
        """ Получает среднюю зарплату по вакансиям """
        self.cur.execute('SELECT AVG(salary) FROM vacancies')
        results = self.cur.fetchall()
        for result in results:
            print(f'Средняя зарплата: {round(float(result[0]), 2)}')
            print('___________________________________________________________')

    def get_vacancies_with_higher_salary(self) -> None:
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        self.cur.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
        results = self.cur.fetchall()
        for result in results:
            print(f'Название вакансии: {result[1]}, Зарплата: {result[2]}, Ссылка: {result[0]}')
            print('_____________________________________________________________________')

    def get_vacancies_with_keyword(self, search_word: str) -> None:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python """
        self.cur.execute("SELECT * FROM vacancies WHERE vacancies_name ILIKE '%" + search_word + "%'")
        results = self.cur.fetchall()
        for result in results:
            if result[2] == 0:
                salary = "Зарплата не указана"
            else:
                salary = result[2]
            print(f'Название вакансии: {result[1]}, Зарплата: {salary}, Ссылка: {result[0]}')
            print('_____________________________________________________________________')

    def __del__(self):
        """ Закрывает соединение с базой данных """
        print("Соединение базы данных отключено")
        self.conn.close()

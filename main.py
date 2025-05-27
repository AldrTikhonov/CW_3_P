import os

from dotenv import load_dotenv

from src.api_module import insert_employers, insert_vacancies
from src.dbmanager import DBManager
from src.utils import (create_db, create_tables, load_employers_to_db,
                       load_vacancies_to_db)

load_dotenv()

dict_data = {
        'host': os.getenv('host'),
        'user':  os.getenv('user'),
        'password': os.getenv('password'),
        'port': os.getenv('port')
    }

EMPLOYER_IDS = [
    '8620',  # rambler
    '1740',  # Яндекс
    '1440683',  # RUTUBE
    '1375441',  # Okko
    '15478',  # VK
    '852361',  # Ростелеком
    '2180',  # ОЗОН
    '3776',  # МТС
    '4219',  # TEL2
    '3127',  # МегаФон
    '39305',  # Газпром нефть
    '3529',  # Сбербанк
    '78638',  # Тинькофф
]


def main():
    print("Приветствуем Вас! В этом приложении вы можете получить информацию о вакансиях с сайта hh.ru")

    while True:

        action = input("Выберите одно из следующих действий и введите его номер:\n\
    1.Получить список всех компаний и количество вакансий у каждой компании.\n\
    2.Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.\n\
    3.Получить среднюю зарплату по вакансиям.\n\
    4.Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n\
    5.Получить список всех вакансий по ключевому слову, например python.\n\
Введите номер: ")

        print("Выполняем запрос...")

        insert_employer = insert_employers(EMPLOYER_IDS)
        insert_vacancie = insert_vacancies(EMPLOYER_IDS)
        create_db(dict_data, 'hh_info')
        create_tables(dict_data, 'hh_info')
        load_employers_to_db(insert_employer, dict_data)
        load_vacancies_to_db(insert_vacancie, dict_data)

        user_db = DBManager(dict_data)

        try:

            if int(action) == 1:
                user_db.get_companies_and_vacancies_count()
                break
            elif int(action) == 2:
                user_db.get_all_vacancies()
                break
            elif int(action) == 3:
                user_db.get_avg_salary()
                break
            elif int(action) == 4:
                user_db.get_vacancies_with_higher_salary()
                break
            elif int(action) == 5:

                keyword_user = input("Введите ключевое слово, например 'менеджер': ")

                user_db.get_vacancies_with_keyword(keyword_user)
                break

        except ValueError:
            print("Введенное вами значение не является числом")
            continue

        else:
            print("Введенное вами значение не соответствует не одному значению")
            continue


if __name__ == '__main__':
    main()

import requests
from dotenv import load_dotenv

load_dotenv()

HH_URL = 'https://api.hh.ru/'

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


def insert_employers(employers_list: list) -> list[dict]:
    """Функция для получения данных о работодателях с сайта hh с помощью API.
    Принимает список работодателей и возвращает словарь с данными о работодателях """

    result_list = []
    for employer in employers_list:
        response = requests.get(HH_URL + 'employers/' + employer)
        result_response = response.json()
        employers_dict = {
            'employers_id': employer,
            'employers_name': result_response.get('name'),
            'number_of_vacancies': result_response.get('open_vacancies'),
        }
        result_list.append(employers_dict)

    return result_list


def insert_vacancies(employers_list: list) -> list[dict]:
    """ Функция для получения данных о вакансиях с сайта hh с помощью API.
    Принимает список работодателей и возвращает словарь с данными о вакансиях """

    result_list = []

    for employer in employers_list:
        params = {
            'employer_id': employer,
            'per_page': 100
        }

        response = requests.get(HH_URL + 'vacancies/', params=params)
        result_response = response.json()

        for item in result_response.get('items'):

            if item.get('salary'):
                salary = item.get('salary').get('from')
            else:
                salary = 0

            vacancies_dict = {
                "url": item.get('alternate_url'),
                'vacancies_name': item.get('name'),
                'salary': salary,
                'employers_id': employer
            }

            result_list.append(vacancies_dict)

    return result_list

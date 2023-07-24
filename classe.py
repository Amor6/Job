from abc import ABC, abstractmethod
from excep import ParsingError
import requests


"""Методы для начальных классов"""
class Engine(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

 #Класс для поиска и отображения вакансий на HH
class HeadHunter(Engine):
    url = 'https://api.hh.ru/vacancies'
    def __init__(self,search):
        self.params = {
            "per_page": 100,
            "page": None,
            "text": search,
            "archived": False,
        }
        self.headers ={
            "User-Agent": "MyImportantApp 1.0"
        }
        self.search = []

#Класс для поиска и отображения вакансий на SJ

class SuperJob(Engine):
    url = 'https://api.superjob.ru/2.0/vacancies'
    def __init__(self,search):
        self.vacancies = None
        self.params = {
            "per_page": 100,
            "page": None,
            "text": search,
            "archived": False,
        }
        self.headers ={
            "X-Api-App-Id": "v3.r.137700321.e138f3c18f37debc346c925698b026217bdc32c1.bd2f714ade865b935973b3d04df6ea19def4bc6d"
        }
        self.search = []
    # Вывод до 200 анкет, если больше 200 ошибка
    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка вывода вакансий! Значение {response.status_code}")
        return response.json()["object"]

   #Вывод на странице информацию о вакансии оплата от и до, название фирмы и т.д
    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.search:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profeesion"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy ["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None
            }

            formatted_vacancy.append(formatted_vacancy)

        return formatted_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []  # Очистка списков вакансии
        for page in range(pages_count):
            page_vacancies= []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page}-", end="")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Вакансий имеется: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break

class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy["employ"]
        self.title = vacancy["title"]
        self.url = vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]
        self.currency_value = vacancy["currency_value"]

    def __str__(self):
        pass

    def __gt__(self):
        pass

class Connector:
    def sort_by_salary_from(self):
        vacancies = self.select()

        vacancies = sorted(vacancies)



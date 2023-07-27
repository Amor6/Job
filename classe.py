from abc import ABC, abstractmethod
import requests

api_key = "v3.r.137700321.e138f3c18f37debc346c925698b026217bdc32c1.bd2f714ade865b935973b3d04df6ea19def4bc6d"


class Engine(ABC):

    @abstractmethod
    def get_vacancies(self, search_query):
        pass

    """"Абстрактный класс и метод"""

class HeadHunter(Engine):

    def get_vacancies(self, search_query, location=None, page=0, per_page=100, only_with_salary=True,
                      salary_min=None, salary_max=None):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": f"NAME:{search_query}",
            "area": location,
            "page": str(page),
            "per_page": str(per_page),
            "only_with_salary": str(only_with_salary),
            "salary_from": str(salary_min),
            "salary_to": str(salary_max)
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            vacancies = []
            for item in data["items"]:
                title = item["name"]
                link = item["alternate_url"]
                salary = item["salary"]["from"]
                description = item.get("snippet", {}).get("requirement", "")

                vacancy = Vacancy(title, link, salary, description)
                vacancies.append(vacancy)

            return vacancies

        """Класс для работы с HH"""

class SuperJob(Engine):

    def get_vacancies(self, search_query, salary_min=None, salary_max=None):

        url = "https://api.superjob.ru/2.33/vacancies"
        headers = {"X-Api-App-Id": api_key}
        params = {"keyword": search_query, "count": 100}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            vacancies = []
            for item in data["objects"]:
                title = item["profession"]
                link = item["link"]
                salary = item["payment_from"] if item.get("payment_from") else "Зарплата не указана"
                description = " ".join([
                    "Образование: " + item.get("education", {}).get("title", "") + ".",
                    "Опыт: " + item.get("experience", {}).get("title", "") + ".",
                    "Место работы: " + item.get("place_of_work", {}).get("title", "") + ".",
                    "Режим работы: " + item.get("type_of_work", {}).get("title", "") + "."
                ])

                vacancy = Vacancy(title, link, salary, description)
                vacancies.append(vacancy)

            return vacancies

    """Класс для работы с SJ"""

class Vacancy:

    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

        """Класс c информацией о вакансии."""

    def __str__(self):

        if self.description:
            return f"Название вакансии: {self.title}\nСсылка: {self.link}\nОплата: {self.salary}\nОписание: {self.description}"
        else:
            return f"Название вакансии: {self.title}\nСсылка: {self.link}\nОплата: {self.salary}\n" \
                   f"Описание: Описание вакансии отсутствует"

    """Представление информации о вакансии"""

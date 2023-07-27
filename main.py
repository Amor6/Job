from classe import SuperJob, HeadHunter
def user_search():
    """
    Функция для взаимодействия с пользователем.
    """
    search_query = input("Название вакансии: ")
    salary_min = input("Минимальная оплата труда: ")
    salary_max = input("Максимальная оплата труда: ")

    hh = HeadHunter()
    sj = SuperJob()

    vacancies_hh = hh.get_vacancies(search_query, salary_min=salary_min,
                                    salary_max=salary_max)
    vacancies_sj = sj.get_vacancies(search_query, salary_min=salary_min, salary_max=salary_max)
    print("\nРезультат по поиску HeadHunter:")
    for vacancy in vacancies_hh:
        print(vacancy)
        print()

    print("Результат по сайту SuperJob:")
    for vacancy in vacancies_sj:
        print(vacancy)
        print()


if __name__ == "__main__":
    user_search()


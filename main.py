from classe import HeadHunter, SuperJob, Connector


def main():
    vacancies_job = []
    # search - Поиск по интересующей вакансии соискателя
    search = "Python"

    hh = HeadHunter(search)
    sj = SuperJob(search)
    for api in (sj, hh):
        api.get_vacancies(pages_count=10)
        vacancies_job.extend(api.get_formatted_vacancies())

    connector = Connector(search=search, vacancies_job=vacancies_job)
#
    while True:
        command = input("list - Показать список вакансий.\n"
                        "paymentmin - Сортировка по минимальной оплате\n"
                        "esc - Выход"
                        )

        if command.lower() == "esc":
            break
        elif command.lower() == "list":
            vacancies = connector.select
        elif command.lower() == "paymentmin":
            vacancies = connector.sorty_by_slary_from()

        for vacancy in vacancies:
            print(vacancy, end="\n")


import requests
import json
from bs4 import BeautifulSoup as bs

vacancies_list = []
for i in range(2):
    url = f'https://kurgan.hh.ru/search/vacancy?area=95&text=python&items_on_page=20&page={i}'

    params = {
        'area': 95,
        'text': 'python',
        'items_on_page': 20,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'serp-item'})

    for vacancy in vacancies:
        vacancy_name = vacancy.find('a', {'class': 'serp-item__title'}).getText()
        vacancy_link = vacancy.find('a', {'class': 'serp-item__title'})['href']
        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary is not None:
            vacancy_salary = vacancy_salary.getText()
            salary_list = vacancy_salary.split(' ')
            if vacancy_salary.startswith('от'):
                min_salary = salary_list[1]
                max_salary = None
                salary_currency = salary_list[2]
            elif vacancy_salary.startswith('до'):
                min_salary = None
                max_salary = salary_list[1]
                salary_currency = salary_list[2]
            else:
                min_salary = salary_list[0]
                max_salary = salary_list[2]
                salary_currency = salary_list[3]
            if min_salary != None:
                min_salary_list = min_salary.split('\u202f')
                min_salary_result = ''
                for el in min_salary_list:
                    min_salary_result += el
                min_salary = min_salary_result
            if max_salary != None:
                max_salary_list = max_salary.split('\u202f')
                max_salary_result = ''
                for el in max_salary_list:
                    max_salary_result += el
                max_salary = max_salary_result
        else:
            min_salary, max_salary, salary_currency = None, None, None

        vacancy_dict = {
            'name': vacancy_name,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'salary_currency': salary_currency,
            'link': vacancy_link,
        }
        vacancies_list.append(vacancy_dict)
data = json.dumps(vacancies_list, ensure_ascii=False)
with open('vacancies_parsing_data.json', 'w') as outfile:
    outfile.write(data)
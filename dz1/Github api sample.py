import requests
import json

def repos_by_username(user_name):
    response = requests.get(f'https://api.github.com/users/{user_name}/repos')
    data = response.json()
    with open('repos.json', 'w') as outfile:
        json.dump(data, outfile)
    for i in range(0,len(data)):
        print("Project Number:",i+1)
        print("Project Name:",data[i]['name'])
        print("Project URL:",data[i]['svn_url'],"\n")

''' 
Для получения данных по закрытым репозиториям надо получить токен для доступа к апи, но получать его не стал.
Код для выполнения ниже, на случай, если это требование обязательное, в теории должно возвращать и закрытые репозитории.
При выполнении первой функции для удобства вывел некоторые данные по каждому репозиторию
'''

def repos_with_token(user_name, token):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'https://api.github.com/users/{user_name}/repos', headers=headers)
    with open('repos_with_token.json', 'w') as outfile:
        json.dump(response.json(), outfile)

repos_by_username('Necris45')

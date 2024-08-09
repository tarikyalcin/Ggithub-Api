import requests

class Github:
    def __init__(self):
        self.api_url = 'https://api.github.com'
        self.token = '******************************************'  # Burada kişisel erişim belirtecini kullanın
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_user(self, username):
        response = requests.get(f'{self.api_url}/users/{username}')
        return response.json()

    def get_repositories(self, username):
        response = requests.get(f'{self.api_url}/users/{username}/repos')
        return response.json()

    def create_repository(self, name, description='This is your first repository', private=False):
        data = {
            "name": name,
            "description": description,
            "homepage": "https://github.com",
            "private": private,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }
        response = requests.post(f'{self.api_url}/user/repos', headers=self.headers, json=data)
        return response.json()

    def delete_repository(self, repo_name):
        response = requests.delete(f'{self.api_url}/repos/{self.get_user()["login"]}/{repo_name}', headers=self.headers)
        if response.status_code == 204:
            return {'message': 'Repository deleted successfully'}
        return response.json()

    def create_issue(self, repo_name, title, body):
        data = {
            "title": title,
            "body": body
        }
        response = requests.post(f'{self.api_url}/repos/{self.get_user()["login"]}/{repo_name}/issues', headers=self.headers, json=data)
        return response.json()

    def close_issue(self, repo_name, issue_number):
        data = {
            "state": "closed"
        }
        response = requests.patch(f'{self.api_url}/repos/{self.get_user()["login"]}/{repo_name}/issues/{issue_number}', headers=self.headers, json=data)
        return response.json()

    def reopen_issue(self, repo_name, issue_number):
        data = {
            "state": "open"
        }
        response = requests.patch(f'{self.api_url}/repos/{self.get_user()["login"]}/{repo_name}/issues/{issue_number}', headers=self.headers, json=data)
        return response.json()

github = Github()

while True:
    secim = input('1- Find User\n2- Get Repositories\n3- Create Repository\n4- Delete Repository\n5- Create Issue\n6- Close Issue\n7- Reopen Issue\n8- Exit\nSeçim: ')

    if secim == '8':
        break
    else:
        if secim == '1':
            username= input('username: ')
            result = github.get_user(username)
            print(f"name: {result['name']} public repos: {result['public_repos']}  followers : {result['followers']}")
        elif secim == '2':
            username = input('username: ')
            result = github.get_repositories(username)
            for repo in result:
                print(repo['name'])
        elif secim == '3':
            name = input('repository name: ')
            description = input('description (optional): ')
            private = input('private (yes/no): ').lower() == 'yes'
            result = github.create_repository(name, description, private)
            print(result)
        elif secim == '4':
            name = input('repository name to delete: ')
            result = github.delete_repository(name)
            print(result)
        elif secim == '5':
            repo_name = input('repository name: ')
            title = input('issue title: ')
            body = input('issue body: ')
            result = github.create_issue(repo_name, title, body)
            print(result)
        elif secim == '6':
            repo_name = input('repository name: ')
            issue_number = input('issue number: ')
            result = github.close_issue(repo_name, issue_number)
            print(result)
        elif secim == '7':
            repo_name = input('repository name: ')
            issue_number = input('issue number: ')
            result = github.reopen_issue(repo_name, issue_number)
            print(result)
        else:
            print('yanlış seçim')
